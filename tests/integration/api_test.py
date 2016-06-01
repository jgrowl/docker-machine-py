import unittest
#
import docker_machine

BUSYBOX = 'busybox:buildroot-2014.02'
EXEC_DRIVER = []


# def exec_driver_is_native():
#     global EXEC_DRIVER
#     if not EXEC_DRIVER:
#         c = docker_client()
#         EXEC_DRIVER = c.info()['ExecutionDriver']
#         c.close()
#     return EXEC_DRIVER.startswith('native')
#
#
def docker_machine_client(**kwargs):
    return docker_machine.Client(**docker_machine_client_kwargs(**kwargs))

def docker_machine_client_kwargs(**kwargs):
    client_kwargs = docker_machine.utils.kwargs_from_env(assert_hostname=False)
    client_kwargs.update(kwargs)
    return client_kwargs
#
#
# def setup_module():
#     warnings.simplefilter('error')
#     c = docker_client()
#     try:
#         c.inspect_image(BUSYBOX)
#     except docker.errors.NotFound:
#         os.write(2, "\npulling busybox\n".encode('utf-8'))
#         for data in c.pull(BUSYBOX, stream=True):
#             data = json.loads(data.decode('utf-8'))
#             os.write(2, ("%c[2K\r" % 27).encode('utf-8'))
#             status = data.get("status")
#             progress = data.get("progress")
#             detail = "{0} - {1}".format(status, progress).encode('utf-8')
#             os.write(2, detail)
#         os.write(2, "\npulled busybox\n".encode('utf-8'))
#
#         # Double make sure we now have busybox
#         c.inspect_image(BUSYBOX)
#     c.close()
#
#
class BaseTestCase(unittest.TestCase):

#     tmp_imgs = []
#     tmp_containers = []
#     tmp_folders = []
#     tmp_volumes = []
#
    def setUp(self):
        #if six.PY2:
        #    self.assertRegex = self.assertRegexpMatches
        #    self.assertCountEqual = self.assertItemsEqual
        self.client = docker_machine_client(timeout=60)
#         self.tmp_imgs = []
#         self.tmp_containers = []
#         self.tmp_folders = []
#         self.tmp_volumes = []
#         self.tmp_networks = []
#
    def tearDown(self):
        return True
#         for img in self.tmp_imgs:
#             try:
#                 self.client.remove_image(img)
#             except docker.errors.APIError:
#                 pass
#         for container in self.tmp_containers:
#             try:
#                 self.client.stop(container, timeout=1)
#                 self.client.remove_container(container)
#             except docker.errors.APIError:
#                 pass
#         for network in self.tmp_networks:
#             try:
#                 self.client.remove_network(network)
#             except docker.errors.APIError:
#                 pass
#         for folder in self.tmp_folders:
#             shutil.rmtree(folder)
#
#         for volume in self.tmp_volumes:
#             try:
#                 self.client.remove_volume(volume)
#             except docker.errors.APIError:
#                 pass
#
#         self.client.close()
#
#     def run_container(self, *args, **kwargs):
#         container = self.client.create_container(*args, **kwargs)
#         self.tmp_containers.append(container)
#         self.client.start(container)
#         exitcode = self.client.wait(container)
#
#         if exitcode != 0:
#             output = self.client.logs(container)
#             raise Exception(
#                 "Container exited with code {}:\n{}"
#                     .format(exitcode, output))
#
#         return container
