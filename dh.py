import gmpy2
import random
class Dh:

    def __init__(self):
        self.p_source = '0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF'
        self.p = 0
        self.g = 0
        self.server_number = 0
        self.init()

    # desc : init method
    def init(self):
        self._genereate_base_info()
        processed_server_num = self._process_server_key()
        dh_mp_map = {
            'p': self.p.digits(10),
            'g': self.g.digits(10),
            'server_number': self.server_number,
            'processed_server_number': processed_server_num.digits(10),
        }
        return dh_mp_map

    #desc : compute key
    def compute_share_key(self, client_number, server_number, p):
        key = gmpy2.powmod(gmpy2.mpz(client_number), gmpy2.mpz(server_number), gmpy2.mpz(p))
        return key.digits(10)

    # generate basic G P number, and also random a int for server-number
    def _genereate_base_info(self):
        self.p = gmpy2.mpz(self.p_source)
        primitive_flag = 0
        while 0 == primitive_flag:
            self.g = gmpy2.mpz_random(gmpy2.random_state(hash(gmpy2.random_state())), gmpy2.sub(self.p, 1))
            powm_ret = gmpy2.powmod(self.g, gmpy2.sub(self.p, 1), self.p)
            if 1 == powm_ret:
                primitive_flag = 1
        self.server_number = random.randint(100, 100000)

    def _process_server_key(self):
        processed_server_number = gmpy2.powmod(self.g, self.server_number, self.p)
        return processed_server_number