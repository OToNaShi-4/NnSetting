from Setting import setting


if __name__ == '__main__':
    setting.cur.my_setting = 2
    print(f'my_setting: {setting.cur.my_setting}')
    print(f'my_setting_2: {setting.cur.my_setting_2}')
    print(f'my_setting_3: {setting.cur.my_setting_3}')