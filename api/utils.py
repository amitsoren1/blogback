import os

def get_url(instance):
    file_name = instance.profile_pic.path.split("/")
    if os.path.exists("/"+file_name[1]+"/"+file_name[2]+"/"+file_name[3]+"/"+file_name[4]+"/"+instance.user.username+"/"+file_name[-1]):
        url = "https://pubgapi.pythonanywhere.com/"+"media/pic_folder/"+f"{instance.user.username}/"+file_name[-1]
        return url
    url = "https://pubgapi.pythonanywhere.com/"+"media/pic_folder/"+file_name[-1]
    return url