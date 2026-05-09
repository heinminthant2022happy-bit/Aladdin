import ctypes
import os

# file path ကို သတ်မှတ်ခြင်း
file_path = os.path.abspath("lucky.so")

def run_so():
    try:
        # .so library ကို load လုပ်ခြင်း
        lib = ctypes.CDLL(file_path)
        
        # .so file အဖြစ်ပြောင်းလိုက်တဲ့အခါ 
        # main code ကို run တဲ့ function name က များသောအားဖြင့် 'main' ဖြစ်တတ်ပါတယ်
        # သို့မဟုတ် programmer သတ်မှတ်ထားတဲ့ နာမည်တစ်ခုခု ဖြစ်ပါလိမ့်မယ်
        
        print("--- Lucky.so ကို စတင်နေပါပြီ ---")
        
        # နမူနာအနေနဲ့ main function ကို ခေါ်ကြည့်ခြင်း
        # (မှတ်ချက် - function name မမှန်ရင် AttributeError တက်ပါလိမ့်မယ်)
        lib.main()
        
    except AttributeError:
        print("အမှား - 'main' ဆိုတဲ့ function ကို ရှာမတွေ့ပါ။")
        print("ဒီ .so file ထဲမှာပါတဲ့ function name ကို သိဖို့ လိုအပ်ပါတယ်။")
    except Exception as e:
        print(f"Error တက်သွားပါတယ်: {e}")

if __name__ == "__main__":
    run_so()
    
