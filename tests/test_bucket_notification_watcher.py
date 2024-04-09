from pytroll_watchers import minio_notification_watcher
from upath import UPath
from contextlib import contextmanager, nullcontext
from posttroll.testing import patched_publisher
from posttroll.message import Message


@contextmanager
def fake_bucket_listener():
    import minio
    from unittest import mock
    FakeMinio = mock.Mock(wraps=minio.Minio)
    FakeMinio.return_value.listen_bucket_notification.return_value = nullcontext(enter_result=records)
    with mock.patch("minio.Minio", FakeMinio):
        yield


def test_generate_paths():
    s3_config = dict(endpoint_url="someendpoint",
                     bucket_name="viirs-data",
                     profile="someprofile")
    with fake_bucket_listener():
        files = list(minio_notification_watcher.file_generator(**s3_config))
    assert len(files) == len(records)
    assert files[0] == UPath("s3://viirs-data/sdr/SVM13_npp_d20240408_t1006227_e1007469_b64498_c20240408102334392250_cspp_dev.h5")


def test_publish_paths():
    s3_config = dict(endpoint_url="someendpoint",
                     bucket_name="viirs-data",
                     profile="someprofile")
    publisher_settings = dict(nameservers=False, port=1979)
    message_settings = dict(subject="/segment/viirs/l1b/", atype="file", data=dict(sensor="viirs"))
    with patched_publisher() as messages:
       with fake_bucket_listener():
              minio_notification_watcher.file_publisher(s3_config=s3_config,
                                                        publisher_config=publisher_settings,
                                                        message_config=message_settings)
    assert len(messages) == len(records)
    message = Message(rawstr=messages[0])
    assert message.data["url"] == "s3://viirs-data/sdr/SVM13_npp_d20240408_t1006227_e1007469_b64498_c20240408102334392250_cspp_dev.h5"
    assert message.data["sensor"] == "viirs"
    assert message.data["fs"] == '{"cls": "s3fs.core.S3FileSystem", "protocol": "s3", "args": []}'


records = \
[{'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:22.544Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470908962A15',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': '9f6fbbf9e2b44509afa922b8d9884682',
                                 'key': 'sdr/SVM13_npp_d20240408_t1006227_e1007469_b64498_c20240408102334392250_cspp_dev.h5',
                                 'sequencer': '17C447090F3AB797',
                                 'size': 22183568,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:22.666Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470912FB48E9',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': 'f92d4f4c1b33b8397fc710aed80ab134',
                                 'key': 'sdr/SVM14_npp_d20240408_t1006227_e1007469_b64498_c20240408102334431798_cspp_dev.h5',
                                 'sequencer': '17C4470916824E6A',
                                 'size': 12357960,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:22.790Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C447091A7B932E',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': '9ffffd85b277704d0b85ecc22d8337ce',
                                 'key': 'sdr/SVM15_npp_d20240408_t1006227_e1007469_b64498_c20240408102334471520_cspp_dev.h5',
                                 'sequencer': '17C447091DE5AEA9',
                                 'size': 12357960,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:22.925Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470921D01846',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': 'a7cea3e72dea4845905922a851fac53c',
                                 'key': 'sdr/SVM16_npp_d20240408_t1006227_e1007469_b64498_c20240408102334509150_cspp_dev.h5',
                                 'sequencer': '17C4470925EB97C5',
                                 'size': 12357960,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:CompleteMultipartUpload',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:25.377Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'content-length': '518',
                                    'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C44709B7B42BA6',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': '6accbb0d6937313fb06b5c09a88b0045-7',
                                 'key': 'sdr/GIMGO_npp_d20240408_t1006227_e1007469_b64498_c20240408102307309287_cspp_dev.h5',
                                 'sequencer': '17C44709B802FBCF',
                                 'size': 324490832,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:CompleteMultipartUpload',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:27.829Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'content-length': '518',
                                    'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470A4A03BE3D',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': '36a554f5a2f344ed5f3ffb7826f0a17a-7',
                                 'key': 'sdr/GITCO_npp_d20240408_t1006227_e1007469_b64498_c20240408102307123064_cspp_dev.h5',
                                 'sequencer': '17C4470A4A2E9DF0',
                                 'size': 324490848,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:28.227Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470A55A65AC6',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': 'c5804716bfa4431e35957308d0266b37',
                                 'key': 'sdr/SVI01_npp_d20240408_t1006227_e1007469_b64498_c20240408102333369886_cspp_dev.h5',
                                 'sequencer': '17C4470A61DAC380',
                                 'size': 49222736,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:28.605Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470A6C179370',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': '6e0465a1a67e401d08312d511e14b797',
                                 'key': 'sdr/SVI02_npp_d20240408_t1006227_e1007469_b64498_c20240408102333521003_cspp_dev.h5',
                                 'sequencer': '17C4470A7877A613',
                                 'size': 49222736,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:28.998Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470A8318051B',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': 'f7a1a9089841e810a4249ee43ac7d344',
                                 'key': 'sdr/SVI03_npp_d20240408_t1006227_e1007469_b64498_c20240408102333616593_cspp_dev.h5',
                                 'sequencer': '17C4470A8FCB6DF1',
                                 'size': 49222736,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:29.475Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470A99695857',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': 'ade56421a7d2b40a27ac32312d496c99',
                                 'key': 'sdr/SVI04_npp_d20240408_t1006227_e1007469_b64498_c20240408102333718056_cspp_dev.h5',
                                 'sequencer': '17C4470AAC4C3A1E',
                                 'size': 49222736,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:29.881Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470AB6F25E72',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': '70c7e8e51601a450c5cd73b3d6e2d57e',
                                 'key': 'sdr/SVI05_npp_d20240408_t1006227_e1007469_b64498_c20240408102333815418_cspp_dev.h5',
                                 'sequencer': '17C4470AC47FA93E',
                                 'size': 49222736,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:CompleteMultipartUpload',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:31.138Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'content-length': '518',
                                    'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470B0F539914',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': '8cfd404cd0a9fde9088ebb8472c0eb7d-4',
                                 'key': 'sdr/GDNBO_npp_d20240408_t1006227_e1007469_b64498_c20240408102306939475_cspp_dev.h5',
                                 'sequencer': '17C4470B0F75A541',
                                 'size': 168652400,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:Put',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:31.293Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470B143343A8',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': '45a903f620151c6e84b3dcabc7662692',
                                 'key': 'sdr/SVDNB_npp_d20240408_t1006227_e1007469_b64498_c20240408102332971066_cspp_dev.h5',
                                 'sequencer': '17C4470B18B25911',
                                 'size': 15662132,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]},
 {'Records': [{'awsRegion': '',
               'eventName': 's3:ObjectCreated:CompleteMultipartUpload',
               'eventSource': 'minio:s3',
               'eventTime': '2024-04-08T10:24:32.244Z',
               'eventVersion': '2.0',
               'requestParameters': {'principalId': 'someuser',
                                     'region': '',
                                     'sourceIPAddress': '172.29.4.164'},
               'responseElements': {'content-length': '518',
                                    'x-amz-id-2': 'b675f5c02385af78c69266a96b22038bea3ecd7423814977a7267fd68ac2bbeb',
                                    'x-amz-request-id': '17C4470B5138A602',
                                    'x-minio-deployment-id': 'a287d091-5b07-4b97-90c7-856aca7e9543',
                                    'x-minio-origin-endpoint': 'https://172.31.28.90:443'},
               's3': {'bucket': {'arn': 'arn:aws:s3:::viirs-data',
                                 'name': 'viirs-data',
                                 'ownerIdentity': {'principalId': 'someuser'}},
                      'configurationId': 'Config',
                      'object': {'contentType': 'application/x-hdf5',
                                 'eTag': 'fea57bce523e03c1cc38d864beb8a3d5-3',
                                 'key': 'sdr/IVCDB_npp_d20240408_t1006227_e1007469_b64498_c20240408102333190566_cspp_dev.h5',
                                 'sequencer': '17C4470B515E6945',
                                 'size': 123520808,
                                 'userMetadata': {'content-type': 'application/x-hdf5'}},
                      's3SchemaVersion': '1.0'},
               'source': {'host': '172.29.4.164',
                          'port': '',
                          'userAgent': 'aiobotocore/2.12.1 md/Botocore#1.34.51 '
                                       'ua/2.0 '
                                       'os/linux#4.18.0-513.18.1.el8_9.x86_64 '
                                       'md/arch#x86_64 lang/python#3.11.8 '
                                       'md/pyimpl#CPython '
                                       'cfg/retry-mode#legacy '
                                       'botocore/1.34.51'},
               'userIdentity': {'principalId': 'someuser'}}]}]
