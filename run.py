import aladdin
import os

if __name__ == "__main__":
    try:
        # .so ဖိုင်ထဲက main function ကို လှမ်းခေါ်တာပါ
        aladdin.main()
    except AttributeError:
        print("Error: main() function ကို ရှာမတွေ့ပါဘူး။")
    except Exception as e:
        print(f"Error: {e}")
      
