# from docker_machine import (
#     Client
#
# )

from .. import base


class DockerClientTest(base.BaseTestCase):
    def setUp(self):
        # self.patcher = mock.patch.multiple(
        #     'docker.Client', get=fake_get, post=fake_post, put=fake_put,
        #     delete=fake_delete
        # )
        # self.patcher.start()

        # self.client = docker_machine.Client()
        return True

        # # Force-clear authconfig to avoid tampering with the tests
        # self.client._cfg = {'Configs': {}}

    def tearDown(self):
        return False
        # self.client.close()
        # self.patcher.stop()

    # def assertIn(self, object, collection):
    #     if six.PY2 and sys.version_info[1] <= 6:
    #         return self.assertTrue(object in collection)
    #     return super(DockerClientTest, self).assertIn(object, collection)
    #
    # def base_create_payload(self, img='busybox', cmd=None):
    #     if not cmd:
    #         cmd = ['true']
    #     return {"Tty": False, "Image": img, "Cmd": cmd,
    #             "AttachStdin": False,
    #             "AttachStderr": True, "AttachStdout": True,
    #             "StdinOnce": False,
    #             "OpenStdin": False, "NetworkDisabled": False,
    #             }