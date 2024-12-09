import pkg_resources

def generate_requirements(file_path="requirements.txt"):
    """
    현재 설치된 패키지를 기반으로 requirements.txt 파일 생성
    """
    try:
        # 현재 설치된 모든 패키지와 버전을 가져오기
        installed_packages = pkg_resources.working_set
        requirements = [f"{pkg.project_name}=={pkg.version}" for pkg in installed_packages]

        # requirements.txt 파일 생성
        with open(file_path, "w") as f:
            f.write("\n".join(requirements))

        print(f"'{file_path}' 파일이 생성되었습니다!")
    except Exception as e:
        print(f"requirements.txt 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    generate_requirements()
