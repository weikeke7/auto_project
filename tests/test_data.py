import pytest
pytest_plugins = 'pytester'
from test_pytest import plugin


@pytest.mark.parametrize("send_when",["every","on_fail"])
def test_send_when(send_when,pytester : pytest.Pytester,tmp_path):#tmp_path 用于生成保存一个临时的配置文件
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"[pytest]\n"
        f"send_when = {send_when}\n"
         "send_address = https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9967d7b8-8a0d-412d-bded-61b74649bb85\n"
    )
    config = pytester.parseconfig(config_path)
    assert  config.getini("send_when") == send_when

    pytester.makepyfile("""
    def test_pass():
        ...
        """)
    pytester.runpytest("-c",str(config_path),"-s")
    if send_when == "every":
        raise Exception



@pytest.mark.parametrize("send_address",["","https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9967d7b8-8a0d-412d-bded-61b74649bb85"])
def test_send_address(send_address,pytester : pytest.Pytester,tmp_path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"[pytest]\n"
        f"send_address = {send_address}\n"
        "send_when = on_fail")
    config = pytester.parseconfig(config_path)
    assert config.getini("send_address") == send_address
    pytester.makepyfile("""
     def test_pass():
         ...
         """)
    pytester.runpytest("-c", str(config_path), "-s")




