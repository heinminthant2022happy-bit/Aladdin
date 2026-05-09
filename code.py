
import Vouchercodes

# Vouchercode.so ထဲမှာပါတဲ့ function တွေကို စတင်အသုံးပြုခြင်း
try:
    # ဥပမာ - Vouchercode ထဲမှာ main() ဆိုတဲ့ function ပါရင် အောက်ပါအတိုင်း ခေါ်သုံးပါ
    Vouchercodes.main() 
    
except AttributeError:
    print("Function အမည် မှားယွင်းနေပါသည်။ .so ဖိုင်ထဲက function အမည်ကို စစ်ဆေးပါ။")
except Exception as e:
    print(f"Error ဖြစ်ပွားမှု: {e}")
    
