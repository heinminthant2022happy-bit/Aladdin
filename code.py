import Vouchercode
import asyncio

if __name__ == "__main__":
    try:
        # Vouchercode.so ထဲက main() function ကို လှမ်းခေါ်တာပါ
        Vouchercode.main()
    except KeyboardInterrupt:
        print("\n[!] Program stopped by user.")
    except Exception as e:
        print(f"\n[!] Error: {e}")

