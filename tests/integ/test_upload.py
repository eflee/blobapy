import requests


def test_presigned_urls(call):
    """Upload and download a blob using presigned urls"""
    # TODO: clean up resources
    data = b"Here is some text"

    put_obj = call("/authorize-put")

    key_name = put_obj["key_name"]
    put_url = put_obj["url"]
    put_response = requests.put(put_url, data=data)
    assert put_response.status_code == 200

    get_url = call("/authorize-get/"+key_name)["url"]
    get_response = requests.get(get_url)
    assert get_response.status_code == 200
    assert get_response.content == data
