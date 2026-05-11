import torch

def check_cuda_environment():
    """
    설치된 PyTorch가 로컬 GPU(RTX 4060)와 정상적으로 통신하는지 검증합니다.
    """
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        cuda_version = torch.version.cuda
        
        print(f"인식된 GPU: {gpu_name}")
        print(f"적용된 CUDA 버전: {cuda_version}")
        print("환경이 성공적으로 구성되었습니다. 양자화 모델 로드를 시작할 수 있습니다.")
    else:
        print("CUDA를 사용할 수 없습니다. 드라이버 설치 상태 및 PyTorch 설치 버전을 다시 확인하십시오.")

if __name__ == "__main__":
    check_cuda_environment()