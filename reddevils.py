#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
#   RED DEVILS TOOL v1.1
#   Dev : NALzz Fsociety
#   Platform : Termux (Python 3)
#   ⚠ For Educational Purposes Only
# ═══════════════════════════════════════════════════════════

import os, sys, time, random, socket, json, re, ssl, threading
import urllib.request, urllib.parse, urllib.error
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context

# ───── COLORS ─────
R  = '\033[91m'
BR = '\033[1;91m'
DR = '\033[31m'
K  = '\033[30m'
W  = '\033[97m'
X  = '\033[0m'
B  = '\033[1m'

UA = "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 RedDevils/1.1"

# ═══════════════════════════════════════════════════════════
#   UTIL
# ═══════════════════════════════════════════════════════════
def clear():
    os.system('clear')

def cprint(t, c=BR, d=0.008):
    for ch in t:
        sys.stdout.write(c + ch); sys.stdout.flush(); time.sleep(d)
    print(X)

def loading():
    clear()
    print()
    cprint("    ╔══════════════════════════════════════════╗", BR, 0.001)
    cprint("    ║      RED DEVILS - SYSTEM BOOTING...      ║", BR, 0.001)
    cprint("    ╚══════════════════════════════════════════╝", BR, 0.001)
    print()
    msgs = [
        "[+] Booting kernel modules",
        "[+] Loading exploit database",
        "[+] Connecting to dark net",
        "[+] Decrypting payloads",
        "[+] Bypassing firewall rules",
        "[+] Injecting attack modules",
        "[+] Starting scanners",
        "[+] Establishing backdoor",
        "[+] Ready to strike",
    ]
    for i in range(1, 101):
        fl = int(45 * i / 100)
        bar = '█' * fl + '░' * (45 - fl)
        m = msgs[min(i * len(msgs) // 101, len(msgs) - 1)]
        sys.stdout.write(f"\r    {BR}[{bar}]{X} {i:3d}%  {DR}{m:<32}{X}")
        sys.stdout.flush()
        time.sleep(random.uniform(0.012, 0.035))
    print("\n")
    time.sleep(0.4)

# ═══════════════════════════════════════════════════════════
#   BANNER
# ═══════════════════════════════════════════════════════════
LOGO = r"""
⢰⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼
⠀⢿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⠴⠶⠖⠒⠛⣿⣽⡟⠛⠓⠒⠶⠶⢤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠴⣯⠏
⠀⠀⢿⣯⣿⠷⣶⣤⡴⣶⣶⣤⠤⠤⣤⣄⡀⠀⣀⡤⠶⠛⠉⠀⠀⠀⠀⠀⠀⠴⠿⣼⠿⠦⠀⠀⠀⠀⠀⠀⠉⠛⠲⢦⣄⣀⣤⣴⠒⣻⣿⣿⢻⣿⣿⣿⠋⣩⣴⠋⠀
⠀⠀⠀⠙⠿⣦⣼⣟⢷⣷⢹⣿⣌⣿⡟⢺⣿⠛⠻⣄⠀⠀⠀⠀⢀⣠⣤⠤⠖⠒⠒⠛⠒⠒⠒⠦⠤⣤⣀⠀⠀⢀⣤⠖⠛⢿⣇⠐⡾⣷⣿⡟⢚⣿⣷⣿⠶⠋⠁⠀⠀
⠀⠀⠀⠀⠀⠈⠙⠛⠛⠻⠾⢿⣾⣮⣗⣸⣿⣆⠄⠀⠙⣦⡖⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢉⣷⡟⠀⡀⢨⣽⣿⣽⣶⢿⡿⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠛⠉⠙⠻⢿⣷⣶⡂⣸⡟⠓⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠛⣧⣄⣿⣾⣿⡋⠉⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠁⠀⠀⠀⣠⠾⣿⣿⣿⣿⡁⠀⠈⢳⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠋⠀⠀⣿⣿⣿⣫⣶⠟⢦⡀⠀⠀⣀⠹⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡼⢿⡷⣾⠀⢀⡞⠁⠀⠹⡄⢻⣿⣿⡆⠀⠘⣿⣦⣤⣀⣀⠀⠀⣀⣀⣤⣶⣿⡯⠀⢀⣾⣿⡿⠋⢀⡞⠀⠀⠙⢆⣀⣿⣻⣯⣷⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡾⠷⠛⢳⡞⣻⠋⠀⠀⠀⠀⢳⡀⢻⣿⣿⣦⣠⣿⡯⣷⡉⣽⠿⠿⠟⠉⣹⡯⣿⣷⣤⣾⣿⣿⠁⠀⣼⠃⠀⠀⠀⠈⠻⡍⠏⠁⠉⢷⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀⠈⡱⠁⠀⠀⠀⠀⠀⠈⢷⠈⣿⣿⣿⠟⣿⣇⡝⣮⡈⠀⠀⠀⣴⡟⠀⢿⡟⢿⣻⣿⣇⠀⣰⠇⠀⠀⠀⠀⠀⠀⠙⡄⠀⠀⠀⢿⡀⠀⠀⠀
⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀⡼⠃⠀⠀⠀⣀⣀⣠⣤⣼⠿⣿⢿⠃⣰⠋⠈⠁⢻⡙⢶⣴⠟⣹⠃⠀⠀⠱⡄⢹⣿⣟⠲⢿⠤⠤⣤⣤⣀⡀⠀⠀⠸⡆⠀⠀⠈⣧⠀⠀⠀
⠀⠀⠀⠀⢠⡏⠀⠀⠀⣰⣃⣤⠖⠋⣉⡡⢆⣠⠟⠁⣼⣿⡿⢸⣇⠶⠊⠀⢸⣷⠛⠉⢳⣿⠀⠀⠐⢶⠹⡌⣿⡿⣆⠈⠱⢦⡐⠦⣄⣉⣙⣶⣄⣹⡀⠀⠀⢸⡇⠀⠀
⠀⠀⠀⠀⣾⠀⠀⢰⣶⣿⣿⣿⡿⢿⣥⣶⣟⣁⣠⣞⣽⠟⡇⢸⣿⡀⣀⡴⠋⢹⡄⠀⣸⣉⣻⣦⣄⣸⣰⡇⣿⢹⣮⣷⣤⣤⣿⠿⠞⣛⣿⣿⣿⣿⡿⠂⠀⠀⢿⠀⠀
⠀⠀⠀⠀⡟⠀⠀⠀⢹⠋⠳⢿⣿⣷⡶⠦⢭⣽⣾⣿⡟⠰⢷⣘⣿⠁⠿⠋⠉⠙⣿⠉⡿⠉⠉⠉⠏⢩⣿⢠⣟⣐⣿⣿⢷⣾⣷⣒⣩⣿⠿⠟⠉⠀⢱⠀⠀⠀⢸⠀⠀
⠀⠀⠀⢠⡇⠀⠀⠀⢸⠀⠀⠀⠈⠙⠻⠿⢿⣿⣿⣿⡟⣠⣾⣳⣽⣷⣦⢠⠄⣖⢹⣿⠃⠃⠠⠂⣰⣿⣿⢿⣧⣄⣻⣿⣿⣛⠟⠛⠋⠀⠀⠀⠀⠀⢸⡄⠀⠀⢸⡇⠀
⠀⠀⠀⢸⡇⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⢀⣸⠿⠋⢻⣿⣿⣿⣿⡽⣽⣾⣿⣦⣬⠞⠏⠀⢤⣼⣿⣿⣿⢱⣿⣿⣿⣿⡆⠈⠙⠲⣤⡀⠀⠀⠀⠀⠀⢸⡇⠀⠀⢸⡇⠀
⠀⠀⠀⠀⡇⢰⣄⣤⣾⠀⠀⠀⢀⣠⠶⠋⠁⠀⢀⣾⣿⢿⣿⣾⣇⢹⡏⣻⣿⠞⠀⠀⠀⠰⣿⣏⣸⡇⣾⣿⣿⣿⣿⣿⠀⠀⠀⠀⠙⠳⢦⣀⠀⠀⢸⢳⣦⡞⢸⡇⠀
⠀⠀⠀⠀⣷⡼⣯⡽⢿⣆⣤⣞⣋⣀⣀⣀⣀⣀⣸⣿⣿⣧⠬⠹⣯⣬⣿⠉⠹⣄⠀⠀⠀⣰⠏⠉⣿⢤⣿⠟⠲⣾⣿⣻⣧⣤⣤⣤⡤⠤⠤⠽⠿⢦⡼⠛⣷⠛⢿⠀⠀
⠀⠀⠀⠀⢻⡄⠘⠃⠀⢿⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣷⣄⠀⢻⣿⠏⢦⠀⠈⠐⠀⠸⡁⠀⡟⠙⣿⠟⠀⣠⣾⣿⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⠀⠙⢀⡿⠀⠀
⠀⠀⠀⠀⠘⣇⠀⠀⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣷⣄⠿⣄⠈⢿⡆⠀⠀⠀⢴⡿⠀⣠⠟⣠⣾⣿⢿⡽⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⣸⠇⠀⠀
⠀⠀⠀⠀⠀⢹⡆⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⢿⣶⡈⢦⢸⡇⠀⢠⠀⢸⡇⠐⢁⣼⣿⢿⣯⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠁⠀⠀⢠⡏⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢶⣿⣿⣳⠀⠀⡇⠀⣼⠀⢸⡇⠀⣜⣿⣹⠶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠁⠀⠀⢀⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠈⢣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⣯⡃⢸⡇⠀⢹⠂⠈⡇⠀⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠞⠀⠀⠀⢠⡞⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠹⣆⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⠷⣼⠃⠀⠀⠀⠀⢷⡰⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⠁⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⣄⠀⠀⠀⠀⠙⢦⣀⠀⠀⠀⠀⠀⠀⠀⢿⣴⣿⣦⣀⣠⣀⣤⣿⣧⢾⠆⠀⠀⠀⠀⠀⠀⠀⣠⠶⠃⠀⠀⠀⢀⡼⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⣆⣉⣷⢦⣀⠀⠀⠀⠀⢸⡜⠿⣷⣿⣿⠿⣽⡿⠛⡞⠀⠀⠀⠀⢀⣠⣴⢊⣁⠀⠀⠀⢀⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣄⣠⢿⣩⡷⡄⠈⠙⠓⠤⢤⣀⣙⣦⣈⣻⣦⣾⣁⣠⣞⣁⣀⠤⠴⠚⠋⣀⣿⣻⣧⡀⣀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠦⣟⡀⠀⠀⠀⠀⠀⠀⠀⠉⠉⢿⡿⠷⣿⢿⡯⠉⠉⠀⠀⠀⠀⠀⠉⠉⣿⡾⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠶⣄⣀⡀⠀⠀⠀⠀⠀⠙⣶⡿⢸⠇⠀⠀⠀⠀⣀⣠⠴⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠒⠒⠲⢾⣟⡥⠿⠒⠒⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

def banner():
    clear()
    print(BR + LOGO + X)
    print(BR + "    ⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘" + X)
    print(f"    {BR}Red Devils{X}")
    print(f"    {W}Version :{R} 1.1{X}")
    print(f"    {W}Tools   :{R} Python{X}")
    print(f"    {W}Dev     :{R} NALzz Fsociety{X}")
    print(BR + "    ⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘" + X)

def banner_small():
    clear()
    print(BR + "    ╔═══════════════════════════════════════════╗" + X)
    print(BR + "    ║         R E D   D E V I L S  v1.1         ║" + X)
    print(BR + "    ╚═══════════════════════════════════════════╝" + X)
    print()

# ═══════════════════════════════════════════════════════════
#   HTTP HELPER
# ═══════════════════════════════════════════════════════════
def http_get(url, timeout=8, extra_headers=None):
    headers = {"User-Agent": UA}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=timeout)

def normalize(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url

# ═══════════════════════════════════════════════════════════
#   MENU 1 - DDoS L7 (SIMULASI)
# ═══════════════════════════════════════════════════════════
def menu_ddos():
    banner_small()
    cprint("    ┌───[ DDoS LAYER 7 ]───┐", BR, 0.001)
    cprint("    [!] Mode SIMULASI - tidak menyerang target asli", DR, 0.003)
    print()
    target = input(f"    {BR}┌─[{W}Target URL{BR}]\n    └──> {X}").strip()
    if not target:
        return
    target = normalize(target)
    try:
        th = int(input(f"    {BR}┌─[{W}Threads (1-200){BR}]\n    └──> {X}") or "20")
    except: th = 20
    th = max(1, min(200, th))
    print()
    cprint(f"    [*] Menyiapkan simulasi flood...", BR, 0.005)
    time.sleep(0.5)
    sent = 0; failed = 0; total = 300
    start = time.time()
    for i in range(total):
        r = random.random()
        if r < 0.72:
            sent += 1; tag = f"{BR}[SENT]{X}"
        elif r < 0.92:
            failed += 1; tag = f"{DR}[FAIL]{X}"
        else:
            tag = f"{W}[WAIT]{X}"
        elapsed = time.time() - start
        rps = (i+1) / max(elapsed, 0.01)
        sys.stdout.write(f"\r    {tag} Sent:{sent:<4} Fail:{failed:<4} Req/s:{rps:5.1f}  [{i+1}/{total}]")
        sys.stdout.flush()
        time.sleep(random.uniform(0.005, 0.03))
    print("\n")
    cprint(f"    [+] Simulasi selesai.", BR, 0.005)
    cprint(f"    [+] Total paket : {sent + failed}", BR, 0.005)
    cprint(f"    [+] Berhasil    : {sent}", BR, 0.005)
    cprint(f"    [+] Gagal       : {failed}", BR, 0.005)
    cprint(f"    [!] Ingat: DDoS asli = tindak pidana!", DR, 0.005)
    input(f"\n    {BR}[ ENTER untuk kembali ]{X}")

# ═══════════════════════════════════════════════════════════
#   MENU 2 - SCAN WEB
# ═══════════════════════════════════════════════════════════
def menu_scanweb():
    banner_small()
    cprint("    ┌───[ SCAN WEB ]───┐", BR, 0.001)
    url = normalize(input(f"    {BR}┌─[{W}URL{BR}]\n    └──> {X}").strip())
    print()
    try:
        t0 = time.time()
        resp = http_get(url)
        dt = (time.time() - t0) * 1000
        body = resp.read(4096)
        print(f"    {BR}[+] Status Code   : {W}{resp.status}{X}")
        print(f"    {BR}[+] Server        : {W}{resp.headers.get('Server','-')}{X}")
        print(f"    {BR}[+] Content-Type  : {W}{resp.headers.get('Content-Type','-')}{X}")
        print(f"    {BR}[+] Powered-By    : {W}{resp.headers.get('X-Powered-By','-')}{X}")
        print(f"    {BR}[+] Response Time : {W}{dt:.1f} ms{X}")
        print(f"    {BR}[+] Content-Length: {W}{len(body)} bytes (sample){X}")
        print()
        cprint("    ── SEMUA HEADERS ──", BR, 0.002)
        for k, v in resp.headers.items():
            print(f"    {DR}•{W} {k}: {R}{v}{X}")
    except Exception as e:
        cprint(f"    [-] Error: {e}", DR, 0.003)
    input(f"\n    {BR}[ ENTER untuk kembali ]{X}")

# ═══════════════════════════════════════════════════════════
#   MENU 3 - INFO IP
# ═══════════════════════════════════════════════════════════
def menu_infoip():
    banner_small()
    cprint("    ┌───[ INFO IP ]───┐", BR, 0.001)
    ip = input(f"    {BR}┌─[{W}IP / Domain{BR}]\n    └──> {X}").strip()
    if not ip: return
    try:
        host = ip
        try:
            resolved = socket.gethostbyname(ip)
            if resolved != ip:
                print(f"    {BR}[+] Resolved: {W}{ip} -> {resolved}{X}")
        except:
            resolved = ip
        url = f"http://ip-api.com/json/{resolved}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        resp = http_get(url, timeout=10)
        data = json.loads(resp.read().decode())
        if data.get("status") == "success":
            print()
            fields = [
                ("IP", data.get("query")),
                ("Country", f"{data.get('country')} ({data.get('countryCode')})"),
                ("Region", data.get("regionName")),
                ("City", data.get("city")),
                ("ZIP", data.get("zip")),
                ("Latitude", data.get("lat")),
                ("Longitude", data.get("lon")),
                ("Timezone", data.get("timezone")),
                ("ISP", data.get("isp")),
                ("Organization", data.get("org")),
                ("AS", data.get("as")),
            ]
            for k, v in fields:
                print(f"    {BR}[+] {W}{k:<14}: {R}{v}{X}")
        else:
            cprint(f"    [-] Gagal: {data.get('message')}", DR, 0.003)
    except Exception as e:
        cprint(f"    [-] Error: {e}", DR, 0.003)
    input(f"\n    {BR}[ ENTER untuk kembali ]{X}")

# ═══════════════════════════════════════════════════════════
#   MENU 4 - SCAN SQL
# ═══════════════════════════════════════════════════════════
SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "microsoft ole db provider for sql server",
    "odbc sql server driver",
    "sqlite error",
    "pg_query()",
    "postgresql query failed",
    "ora-01756",
    "mysql_fetch_array()",
    "supplied argument is not a valid mysql",
]

def menu_scansql():
    banner_small()
    cprint("    ┌───[ SCAN SQL ]───┐", BR, 0.001)
    cprint("    [!] Deteksi celah SQL Injection sederhana", DR, 0.003)
    print()
    url = normalize(input(f"    {BR}┌─[{W}URL (dengan parameter, contoh: site.com/page?id=1){BR}]\n    └──> {X}").strip())
    if not url or "?" not in url:
        cprint("    [-] URL harus mengandung parameter '?' ", DR, 0.003)
        input(f"\n    {BR}[ ENTER ]{X}")
        return
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    print()
    cprint(f"    [*] Parameter terdeteksi: {len(params)}", BR, 0.005)
    payloads = ["'", "\"", "' OR '1'='1", "1' AND SLEEP(0)--", "') OR ('1'='1"]
    for pname in params:
        print(f"\n    {BR}[*] Testing parameter: {W}{pname}{X}")
        for pay in payloads:
            test_params = dict(params)
            test_params[pname] = [params[pname][0] + pay]
            new_q = urllib.parse.urlencode(test_params, doseq=True)
            test_url = urllib.parse.urlunparse(parsed._replace(query=new_q))
            sys.stdout.write(f"      {DR}→ {pay[:30]:<30} ... {X}")
            sys.stdout.flush()
            try:
                r = http_get(test_url, timeout=8)
                body = r.read().decode("utf-8", errors="ignore").lower()
                found = any(e in body for e in SQL_ERRORS)
                if found:
                    print(f"{BR}[VULNERABLE!]{X}")
                else:
                    print(f"{W}[ok]{X}")
            except urllib.error.HTTPError as e:
                print(f"{W}[HTTP {e.code}]{X}")
            except Exception as e:
                print(f"{DR}[err]{X}")
    print()
    cprint("    [+] Scan SQL selesai.", BR, 0.005)
    input(f"\n    {BR}[ ENTER untuk kembali ]{X}")

# ═══════════════════════════════════════════════════════════
#   MENU 5 - SCAN VULN WEB
# ═══════════════════════════════════════════════════════════
def menu_vuln():
    banner_small()
    cprint("    ┌───[ SCAN VULN WEB ]───┐", BR, 0.001)
    url = normalize(input(f"    {BR}┌─[{W}URL{BR}]\n    └──> {X}").strip())
    if not url: return
    print()
    try:
        resp = http_get(url)
        h = resp.headers
    except Exception as e:
        cprint(f"    [-] Error: {e}", DR, 0.003)
        input(f"\n    {BR}[ ENTER ]{X}"); return

    cprint(f"    [*] Checking security headers...", BR, 0.005)
    checks = {
        "Strict-Transport-Security": "HSTS tidak aktif (rawan SSL strip)",
        "X-Frame-Options": "Clickjacking protection tidak ada",
        "X-Content-Type-Options": "MIME sniffing tidak dicegah",
        "Content-Security-Policy": "CSP tidak ada (rawan XSS)",
        "Referrer-Policy": "Referrer policy tidak ada",
        "Permissions-Policy": "Permissions policy tidak ada",
    }
    vuln_count = 0
    for k, msg in checks.items():
        if k.lower() not in [x.lower() for x in h.keys()]:
            print(f"    {BR}[!] {W}{k:<28} {DR}MISSING - {msg}{X}")
            vuln_count += 1
        else:
            print(f"    {BR}[+] {W}{k:<28} {R}OK{X}")
    print()
    cprint(f"    [*] Check file sensitif...", BR, 0.005)
    base = "{u.scheme}://{u.netloc}".format(u=urllib.parse.urlparse(url))
    sensitive = [".git/config", ".env", "robots.txt", "sitemap.xml",
                 "admin/", "wp-admin/", "backup.zip", "config.php.bak",
                 "phpinfo.php", ".htaccess"]
    for p in sensitive:
        test_url = f"{base}/{p}"
        try:
            r = http_get(test_url, timeout=5)
            code = r.status
            if code == 200:
                print(f"    {BR}[!] {W}{p:<20} {R}EXPOSED (200){X}")
                vuln_count += 1
            else:
                print(f"    {W}[+] {p:<20} {DR}{code}{X}")
        except urllib.error.HTTPError as e:
            print(f"    {W}[+] {p:<20} {DR}{e.code}{X}")
        except Exception:
            print(f"    {W}[+] {p:<20} {DR}err{X}")
    print()
    cprint(f"    [=] Total potensi vuln: {vuln_count}", BR, 0.005)
    input(f"\n    {BR}[ ENTER untuk kembali ]{X}")

# ═══════════════════════════════════════════════════════════
#   MENU 6 - DETECT URL
# ═══════════════════════════════════════════════════════════
def menu_detecturl():
    banner_small()
    cprint("    ┌───[ DETECT URLS ]───┐", BR, 0.001)
    url = normalize(input(f"    {BR}┌─[{W}URL{BR}]\n    └──> {X}").strip())
    if not url: return
    print()
    try:
        resp = http_get(url)
        html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        cprint(f"    [-] Error: {e}", DR, 0.003)
        input(f"\n    {BR}[ ENTER ]{X}"); return

    parsed = urllib.parse.urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html, re.I)
    srcs  = re.findall(r'src=["\']([^"\']+)["\']', html, re.I)
    actions = re.findall(r'action=["\']([^"\']+)["\']', html, re.I)
    links = set()
    for l in hrefs + srcs + actions:
        if l.startswith(("javascript:", "#", "mailto:", "tel:")):
            continue
        full = urllib.parse.urljoin(base, l)
        links.add(full)
    print(f"    {BR}[+] Total URL ditemukan: {W}{len(links)}{X}\n")
    for i, l in enumerate(sorted(links), 1):
        print(f"    {BR}[{i:03d}]{W} {l}{X}")
    input(f"\n    {BR}[ ENTER untuk kembali ]{X}")

# ═══════════════════════════════════════════════════════════
#   MENU 7 - TANAM WEB SHELL (SIMULASI)
# ═══════════════════════════════════════════════════════════
def menu_shell():
    banner_small()
    cprint("    ┌───[ TANAM WEB SHELL ]───┐", BR, 0.001)
    cprint("    [!] Mode SIMULASI - tidak menanam apapun", DR, 0.003)
    cprint("    [!] Menanam shell tanpa izin = PIDANA!", DR, 0.003)
    print()
    url = input(f"    {BR}┌─[{W}Target URL{BR}]\n    └──> {X}").strip()
    if not url: return
    shell_name = input(f"    {BR}┌─[{W}Nama shell{BR}]\n    └──> {X}").strip() or "devils.php"
    print()
    steps = [
        "Memeriksa celah upload",
        "Mencoba bypass filter extension",
        "Mengubah header MIME",
        "Menyisipkan payload",
        "Mengakses shell",
        "Verifikasi akses",
    ]
    for i, s in enumerate(steps, 1):
        for _ in range(random.randint(3, 7)):
            sys.stdout.write(f"\r    {BR}[{i}/{len(steps)}]{W} {s}...{X}")
            sys.stdout.flush()
            time.sleep(random.uniform(0.05, 0.15))
        print(f"\r    {BR}[{i}/{len(steps)}]{W} {s}... {DR}[SIMULATED]{X}")
    print()
    cprint(f"    [✓] Simulasi selesai. Shell: {shell_name}", BR, 0.005)
    cprint(f"    [!] Ingat: ini hanya demo edukasi.", DR, 0.005)
    input(f"\n    {BR}[ ENTER untuk kembali ]{X}")

# ═══════════════════════════════════════════════════════════
#   MENU
# ═══════════════════════════════════════════════════════════
def show_menu():
    print(f"    {BR}[{W}01{BR}]{W} DDoS Layer 7            {DR}(simulasi){X}")
    print(f"    {BR}[{W}02{BR}]{W} Scan Web{X}")
    print(f"    {BR}[{W}03{BR}]{W} Info IP{X}")
    print(f"    {BR}[{W}04{BR}]{W} Scan SQL{X}")
    print(f"    {BR}[{W}05{BR}]{W} Scan Vuln Web{X}")
    print(f"    {BR}[{W}06{BR}]{W} Detect Semua URL{X}")
    print(f"    {BR}[{W}07{BR}]{W} Tanam Web Shell         {DR}(simulasi){X}")
    print(f"    {BR}[{W}00{BR}]{W} Exit{X}")
    print()
    print(BR + "    ⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘" + X)

def main():
    loading()
    while True:
        banner()
        show_menu()
        try:
            ch = input(f"\n    {BR}┌─[{W}RED DEVILS{BR}]\n    └──> {X}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            cprint("    [!] Keluar...", DR, 0.01)
            break
        if ch in ("1", "01"):
            menu_ddos()
        elif ch in ("2", "02"):
            menu_scanweb()
        elif ch in ("3", "03"):
            menu_infoip()
        elif ch in ("4", "04"):
            menu_scansql()
        elif ch in ("5", "05"):
            menu_vuln()
        elif ch in ("6", "06"):
            menu_detecturl()
        elif ch in ("7", "07"):
            menu_shell()
        elif ch in ("0", "00", "exit", "quit"):
            print()
            cprint("    [✓] Terima kasih telah menggunakan Red Devils", BR, 0.01)
            cprint("    [✓] Stay safe, stay legal!", BR, 0.01)
            break
        else:
            cprint("    [-] Pilihan tidak valid!", DR, 0.005)
            time.sleep(0.8)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        cprint("    [!] Dibatalkan user.", DR, 0.01)
        sys.exit(0)
