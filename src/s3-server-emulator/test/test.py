import socket

class S3ClientEmulator(object):
    def __init__(self):
        pass
    def download_file(self, bucket, key, filename):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('172.17.0.1', 6000))
        s.send(('D' + key).encode('utf-8'))
        response = s.recv(1048576)
        flag = response[0].decode('utf-8')
        responseBody = response[1:]
        if flag == 'Y':
            with open(filename, 'wb') as f:
                f.write(responseBody)
            s.close()
        elif flag == 'N':
            raise RuntimeError('download request is denied')
            s.close()
        else:
            raise RuntimeError('unknown error')
            s.close()
    def upload_file(self, filename, bucket, key):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('172.17.0.1', 6000))
        with open(filename, 'rb') as f:
            s.send(('U' + key + '*').encode('utf-8') + f.read())
        s.close()

def main():
    cli = S3ClientEmulator()
    cli.download_file('', 'download-src', 'download-dest')
    cli.upload_file('upload-src', '', 'upload-dest')

main()
