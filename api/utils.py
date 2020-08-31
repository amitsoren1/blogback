def get_url(instance):
    file_name = instance.profile_pic.path.split("/")[-1]
    url = "https://pubgapi.pythonanywhere.com/"+"media/pic_folder/"+f"{instance.user.username}/"+file_name
    return url