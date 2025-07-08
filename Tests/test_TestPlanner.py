import sys
import os
from unittest.mock import Mock
import pytest
import requests

# Adjust the paths according to your project structure
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..', 'Sources/RAGAPIServices'))
sys.path.append(project_dir)

from fastapi.testclient import TestClient
from Sources.RAGAPIServices.main import app
from Sources.RAGAPIServices.Routers.TestPlannerRouter import TestPlannerRouter

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def base_url():
    return "http://btfubuntu016.boi.rd.hpicorp.net:3489/stage3webservice"

@pytest.fixture
def query_params():
       return {"RegressionConfigID": "61f9027617fc865f7186b4e5"}

@pytest.fixture
def mock_regressionconfig_data():
    return { "Data": {
        "_id": "61f9027617fc865f7186b4e5",
        "ProductGroup": "selene",
        "MakeTarget": "selene",
        "RuntimeProduct": "SeleneFDW",
        "buildphase": "mp1",
        "Branch": "24s",
        "DUTType": "sim",
        "Active": True,
        "Priority": 2,
        "ExecutionNeedCount": 0,
        "LastExecutionTime": "2020-07-21T11:08:37.179073",
        "created_at": "2020-07-21T11:14:31.631483",
        "updated_at": "2024-02-29T05:40:37.437632",
        "Stage2BuildCheck": False,
        "BuildInfo": {
            "Architecture": "x86_32",
            "OS": "linux",
            "CodeBase": "dune",
            "Variant": "debug",
            "skuname": "selene-linux-x86_32-debug",
            "ProductFamily": "homepro",
            "Product": "selene",
            "RuntimeProduct": "SeleneFDW",
            "buildphase": "mp1",
            "TarFiles": {
                "SimTar": "artifacts.bcn.rd.hpicorp.net/artifacts/builds/{data[Codebase]}_{data[Branch]}_{data[Family]}_{data[Platform]}_{data[Revision]}/{data[OS]}-{data[Architecture]}-{data[Variant]}/{data[Family]}/archive/{data[Platform]}-{data[Codebase]}-{data[OS]}-{data[Architecture]}-{data[Family]}-{data[Product]}-{data[Variant]}.tar.xz",
                "TestTar": "artifacts.bcn.rd.hpicorp.net/artifacts/builds/{data[Codebase]}_{data[Branch]}_{data[Family]}_{data[Platform]}_{data[Revision]}/{data[OS]}-{data[Architecture]}-{data[Variant]}/{data[Family]}/archive/test-{data[Codebase]}-{data[OS]}-{data[Architecture]}-{data[Family]}-{data[Variant]}-int-test.tar.xz"
            }
        },
        "Obsolete": False,
        "RegressionPool": "platform",
        "RegressionPoolQueue": "DuneShadowSimRegressionTestTracksQueue",
        "fallback_revision_limit": 10,
        "disable_pass_logs": True,
        "delivery_teams": ["All"]
    }
        
    }

def test_get_regression_config_details_success(mocker, base_url,mock_regressionconfig_data):
    # Create an instance of the TestPlannerRouter class
    router = TestPlannerRouter(prefix="/api/v1")

    # Define the base_url and query_params for the test
    url = base_url + "/v1/config"
    query_params = {"RegressionConfigID": "61f9027617fc865f7186b4e5"}

    # Mock the response of the requests.get call
    mock_response = Mock()
    expected_data = mock_regressionconfig_data
    mock_response.status_code = 200
    mock_response.json.return_value = expected_data

    # Use mocker to patch the requests.get method
    mocker.patch("requests.get", return_value=mock_response)

    # Call the method under test
    result = router.getRegressionconfigDetails(url, query_params)

    # Assert that the method returns the expected data
    assert result == expected_data['Data']
    


@pytest.fixture
def delivery_teams_query_params():
    return {"RegressionPool": "platform"}

@pytest.fixture
def mock_regressionpool_deliveryteams_data():
    return {
        "Data": ['Connectivity', 'CoreFramework', 'FWsolns', 'MediaSupplies', 'PDLJobPQ', 'ViewFramework', 'WalkupApps']
    }

@pytest.fixture
def test_planner_router():
    return TestPlannerRouter(prefix="/api/v1")

def test_get_regression_pool_delivery_teams_success(mocker, base_url, test_planner_router, delivery_teams_query_params, mock_regressionpool_deliveryteams_data):
    # Mock the response of the requests.get call

    mock_response = Mock()
    expected_data = mock_regressionpool_deliveryteams_data
    mock_response.status_code = 200
    mock_response.json.return_value = expected_data

    # Use mocker to patch the requests.get method
    mocker.patch("requests.get", return_value=mock_response)

    # Call the method under test
    result = test_planner_router.getRegressionpoolDeliveryteams(base_url, delivery_teams_query_params)

    # Assert that the method returns the expected data
    assert result == expected_data['Data']



def test_single_job_creation(client):
    query_params = {
        "regression_config_id": "61f9027617fc865f7186b4e5",
        "revision": "6.25.0.474",
        "test_track_type": "Regression",
        "duration": "0h",
        "batch_size": 1,
        "limit": 1,
        "upload_to_db": True
    }
    print(client.base_url)
    response = client.get("/api/v1/testplanner/", params=query_params)
    # data = response.json()['TestTracks']
    print("##################################################################################################################")
    data = response.json()['TestTracks']
    for track in data:
        print(track)
    assert response.status_code in [200, 201]
    assert len(data) == 1


def test_without_parameters(client):
    query_params = {
        "regression_config_id": "61f9027617fc865f7186b4e5",
        "revision": "6.25.0.474",
        "test_track_type": "Regression",
        "duration": "0h",
        "batch_size": 1,
        "limit": 1,
        "upload_to_db": True
    }
    print(client.base_url)
    response = client.get("/api/v1/testplanner/")
    # data = response.json()['TestTracks']
    assert response.status_code == 422

@pytest.fixture
def filterToSend():
    return {'branch': '24s', 'duration': 0, 'dutType': 'Simulator', 'product': 'selene', 'limit': '1', 'runtimeProduct': 'SeleneFDW'}

@pytest.fixture
def getTestcasesOutput():
    return [
        {
            '_id': '623c172cb705fb32289378fb',
            'guid': 'f249fdb6-62c5-4790-8911-36f68769472e',
            'codebase': 'Dune',
            'obsolete': False,
            'deliveryTeam': 'LFP',
            'repobranch': '24s',
            'testSchema': '1.2',
            'testArgs': [],
            'title': 'test_ews_modify_user_permission',
            'name': 'test_ews_modify_user_permission',
            'testFramework': 'TUF',
            'stability': 'Stable',
            'timeout': 120,
            'asset': 'EWS',
            'package': '',
            'version': '',
            'classification': 'System',
            'ptoLevel': '',
            'lastModTime': '2024-05-07 11:05:43.390000',
            'featureTeam': 'LFP_EWS',
            'resources': [],
            'test_tier': 2,
            'weight': 2356.0,
            'is_manual': 'False',
            'path': '\\src\\test\\tests\\security\\accountManagement\\DeviceUser\\test_ews_modify_user_permissions.py',
            'file': {
                'assembly': '',
                'file': 'test_ews_modify_user_permissions.py',
                'repo': 'git@github-partner.azc.ext.hp.com/jedi/dune.git',
                'branch': '24s',
                'test_path': '\\src\\test\\tests\\security\\accountManagement\\DeviceUser'
            },
            'test_framework_settings': {},
            'devices_under_test': [
                {
                    'id': '0',
                    'type': ['Simulator'],
                    'configurations_and_settings': {
                        'Authentication': ['LocalDevice'],
                        'WebServices': ['CDM', 'EWS'],
                        'Security': ['Syslog']
                    }
                }
            ],
            'testsourcename': 'test_ews_modify_user_permission',
            'external_files': {},
            'last_executed_date': None
        }
    ]
@pytest.fixture
def brainproxy_base_url():
    return "http://btfubuntu001.boi.rd.hpicorp.net:3486"

def test_get_testcases(mocker, brainproxy_base_url, filterToSend,getTestcasesOutput):
    router = TestPlannerRouter(prefix="/api/v1")

    # Define the base_url and query_params for the test
    url = brainproxy_base_url + "/v1/regression/tests"
    query_params = filterToSend

    # Mock the response of the requests.get call
    mock_response = Mock()
    expected_data = mock_regressionconfig_data
    mock_response.status_code = 200
    mock_response.json.return_value = expected_data

    # Use mocker to patch the requests.get method
    mocker.patch("requests.get", return_value=mock_response)

    # Call the method under test
    result = router.getTestCases(query_params)
    print("\n\n\n\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n\n\n")
    print(result)
    # Assert that the method returns the expected data
    assert result == getTestcasesOutput

if __name__ == "__main__":
    pytest.main()
