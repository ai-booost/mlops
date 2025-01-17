## Feature Batch Runner 문서

이 문서는 `feature_batch` 스크립트의 동작 방식과 구성 요소를 설명합니다. 이 스크립트는 데이터를 처리하고, 피처 레지스트리를 통해 데이터를 배치 처리하는 역할을 합니다.

### 1. 전체 흐름

이 스크립트는 크게 두 가지 주요 파일로 나누어집니다. 첫 번째 파일은 `FeatureRegistry`와 `LocalFeatureStore`를 사용하여 피처 레지스트리를 처리하는 역할을 하며, 두 번째 파일은 데이터 파이프라인과 관련된 파일로, 다양한 종류의 데이터를 로드하고 처리합니다.

### 2. 구성 요소

#### 2.1 `feature_batch.py` 
이 파일은 데이터를 배치 방식으로 처리하는 기능을 수행합니다. `FeatureRegistry`와 `LocalFeatureStore`를 사용하여 데이터를 로드하고 처리 후, 피처 스토어에 저장합니다.

##### 2.1.1 주요 클래스 및 메서드

- **FeatureRegistry**:
    - 피처 레지스트리 클래스는 데이터를 처리하고 이를 저장하는 기능을 합니다.
    - `batch_all_data()`: 전체 데이터를 불러와 처리한 후 저장합니다.
    - `batch_daily_data()`: 일별 데이터를 불러와 처리한 후 저장합니다.
  
- **LocalFeatureStore**:
    - 로컬 환경에서 피처 데이터를 저장하는 역할을 하는 클래스입니다.
  
- **DataPipeline**:
    - 데이터를 로드하고 처리하는 역할을 하며, `run_pipeline()` 메서드를 통해 데이터를 변환 및 처리합니다.

### 3. 사용 방법

#### 3.1 `FeatureRegistry` 클래스 사용

- **load_all_data**: 전체 데이터를 로드하여 처리 후 저장합니다.
- **load_daily_data**: 일별 데이터를 로드하여 처리 후 저장합니다.

#### 3.2 배치 실행 예시

1. **전체 데이터 로드 및 처리**:
   ```bash
   python feature_registry.py load_all_data
   ```

2. **일별 데이터 로드 및 처리**:
   ```bash
   python feature_registry.py load_daily_data
   ```
