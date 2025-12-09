import psutil
import time
import os
from datetime import datetime

# ==========================================
# 사용자 설정 (로그 저장 경로 등)
# ==========================================
LOG_DIR = "C:\\Kiosk_Logs"  # 로그 저장할 폴더
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

safe_now = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f"memory_overflow_log{safe_now}.txt")


def get_top_processes(limit=10):
    """메모리를 가장 많이 사용하는 프로세스 TOP N을 가져옵니다."""
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            # memory_info().rss : 실제 물리 메모리 점유량 (Resident Set Size)
            mem_bytes = p.info['memory_info'].rss
            procs.append({
                'pid': p.info['pid'],
                'name': p.info['name'],
                'memory': mem_bytes,
                'memory_mb': mem_bytes / (1024 * 1024)  # MB 단위 변환
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 메모리 사용량 내림차순 정렬
    procs.sort(key=lambda x: x['memory'], reverse=True)
    return procs[:limit]


def start_monitoring():
    print("=== 실시간 메모리 감시 프로그램 ===")

    # 1. 임계값(GB) 입력 받기
    while True:
        try:
            threshold_gb = float(input("경고를 기록할 기준 메모리 용량을 입력하세요 (단위: GB): "))
            break
        except ValueError:
            print("숫자만 입력해주세요.")

    # GB -> Bytes 변환
    threshold_bytes = threshold_gb * 1024 * 1024 * 1024

    print(f"\n[감시 시작] 메모리 사용량이 {threshold_gb}GB ({threshold_bytes / 1024 / 1024:,.0f}MB)를 넘으면 기록합니다.")
    print(f"로그 파일 위치: {LOG_FILE}")
    print("종료하려면 Ctrl+C를 누르세요.\n")

    try:
        while True:
            # 2. 현재 전체 메모리 사용량 체크
            mem = psutil.virtual_memory()
            used_memory = mem.used

            # 3. 기준치 초과 시 기록
            if used_memory >= threshold_bytes:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                used_gb = used_memory / (1024 * 1024 * 1024)
                total_gb = mem.total / (1024 * 1024 * 1024)

                alert_msg = f"[WARNING] {now} - 메모리 초과 감지! 현재: {used_gb:.2f}GB / 기준: {threshold_gb}GB"

                print(alert_msg)  # 화면 출력

                # 로그 파일에 쓰기
                with open(LOG_FILE, "a", encoding="utf-8") as f:
                    f.write("\n" + "=" * 50 + "\n")
                    f.write(f"{alert_msg}\n")
                    f.write(f"전체 시스템 메모리: {used_gb:.4f}GB / {total_gb:.2f}GB ({mem.percent}%)\n")
                    f.write("-" * 50 + "\n")
                    f.write(f"{'PID':<8} {'Process Name':<25} {'Memory (MB)':<15}\n")
                    f.write("-" * 50 + "\n")

                    # 상위 프로세스 기록
                    top_procs = get_top_processes(10)
                    for p in top_procs:
                        f.write(f"{p['pid']:<8} {p['name']:<25} {p['memory_mb']:,.2f} MB\n")

                    f.write("=" * 50 + "\n")

                # 로그가 너무 빨리 쌓이지 않게 1분 대기 (쿨타임)
                print("   -> 로그 기록 완료. 60초간 대기합니다...")
                time.sleep(60)

            else:
                # 정상일 때는 3초마다 체크
                # print(f"정상.. 현재: {used_memory / 1024**3:.2f}GB", end='\r') # 모니터링용 (선택)
                time.sleep(3)

    except KeyboardInterrupt:
        print("\n감시를 종료합니다.")


if __name__ == "__main__":
    start_monitoring()