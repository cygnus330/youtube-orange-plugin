import pkg_resources
import subprocess
import sys


def uninstall_all_packages():
    # 설치된 모든 패키지 목록 가져오기 (pip 자체는 제외)
    installed_packages = [pkg.key for pkg in pkg_resources.working_set if pkg.key != 'pip']

    if not installed_packages:
        print("삭제할 패키지가 없습니다.")
        return

    # 사용자 확인
    confirm = input(f"다음 패키지들을 모두 삭제하시겠습니까? (y/n)\n{', '.join(installed_packages)}\n")
    if confirm.lower() != 'y':
        print("작업이 취소되었습니다.")
        return

    # 패키지 삭제
    for package in installed_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package])
            print(f"{package} 삭제 완료")
        except subprocess.CalledProcessError:
            print(f"{package} 삭제 중 오류 발생")


if __name__ == "__main__":
    uninstall_all_packages()