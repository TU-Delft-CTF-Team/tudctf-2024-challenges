using System;

namespace Glasses {
    public static class Program {
        private static string encryptedCore = "\x23\x3d\x3d\x0b\x31\x74\x0b\x3f\x70\x22\x61\x1b\x24\x27\x74\x33\x27\x70\x39\x38\x77\x26\x60\x1b\x23\x66\x70\x26\x0a\x23\x38\x61\x37\x27\x66\x71";
        private static string key = "TUD";

        public static void Main(string[] args) {
            if(args.Length != 1) {
                Console.WriteLine("Usage: ./Glasses.exe <flag>");
                return;
            }

            var flag = args[0];
            var prefix = flag.Substring(0, 7);
            var suffix = flag[flag.Length - 1];
            var core = flag.Substring(7, flag.Length - 1 - 7);

            if(prefix != "TUDCTF{" || suffix != '}') {
                Console.WriteLine("Invalid format");
                return;
            }

            if(core.Length != encryptedCore.Length) {
                Console.WriteLine("Invalid flag");
                return;
            }

            for(int i = 0; i < core.Length; i++) {
                char c = core[i];
                char k = key[i % key.Length];
                if((c ^ k) != encryptedCore[i]) {
                    Console.WriteLine("Invalid flag");
                    return;
                }
            }

            Console.WriteLine("Congratulations!");
        }
    }
}