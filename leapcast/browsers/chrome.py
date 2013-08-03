import shlex
import subprocess
import tempfile
import shutil

from leapcast.environment import Environment

class Chrome(object):

    def __init__(self, appurl):
        if not Environment.fullscreen:
            appurl = '--app="%s"' % appurl
        command_line = '''%s --incognito --no-first-run --kiosk --user-agent="%s"  %s''' % (
            Environment.chrome, Environment.user_agent, appurl)
        args = shlex.split(command_line)
        self.tmpdir = tempfile.mkdtemp(prefix="leapcast-")
        args.append('--user-data-dir=%s' % self.tmpdir)
        self.pid = subprocess.Popen(args)

    def destroy(self):
        self.pid.terminate()
        self.pid.wait()
        shutil.rmtree(self.tmpdir)

    def is_running(self):
        return self.pid.poll() is None

    def __bool__(self):
        return self.is_running()
