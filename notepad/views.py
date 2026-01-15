from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from urllib.parse import quote
import json
import os
from datetime import datetime

def get_user_notes_file(username):
    return settings.NOTES_DIR / f'{username}_notes.json'

def load_notes(username):
    file_path = get_user_notes_file(username)
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_notes(username, notes):
    file_path = get_user_notes_file(username)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def landing_page(request):
    # Jika user sudah login, redirect ke dashboard
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')

def login_view(request):
    # Jika sudah login, redirect ke dashboard
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang kembali, {username}!')
            return redirect('home')  # Redirect ke dashboard setelah login
        else:
            messages.error(request, 'Username atau password salah!')
    
    return render(request, 'login.html')

def register_view(request):
    # Jika sudah login, redirect ke dashboard
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Password tidak cocok!')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
        elif len(password) < 8:
            messages.error(request, 'Password harus minimal 8 karakter!')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('login')
    
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Anda telah keluar. Sampai jumpa!')
    return redirect('landing')  # Redirect ke landing page setelah logout

@login_required
def home(request):
    notes = load_notes(request.user.username)
    notes.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
    return render(request, 'home.html', {'notes': notes})

@login_required
def create_note(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled')
        content = request.POST.get('content', '')
        
        notes = load_notes(request.user.username)
        new_id = max([n['id'] for n in notes], default=0) + 1
        
        new_note = {
            'id': new_id,
            'title': title,
            'content': content,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        notes.append(new_note)
        save_notes(request.user.username, notes)
        messages.success(request, 'Catatan berhasil dibuat!')
        return redirect('note_detail', note_id=new_id)
    
    return render(request, 'create_note.html')

@login_required
def note_detail(request, note_id):
    notes = load_notes(request.user.username)
    note = next((n for n in notes if n['id'] == note_id), None)
    
    if not note:
        messages.error(request, 'Catatan tidak ditemukan!')
        return redirect('home')
    
    if request.method == 'POST':
        note['title'] = request.POST.get('title', note['title'])
        note['content'] = request.POST.get('content', note['content'])
        note['updated_at'] = datetime.now().isoformat()
        save_notes(request.user.username, notes)
        messages.success(request, 'Catatan berhasil diperbarui!')
    
    return render(request, 'note_detail.html', {'note': note})

@login_required
def delete_note(request, note_id):
    if request.method == 'POST':
        notes = load_notes(request.user.username)
        notes = [n for n in notes if n['id'] != note_id]
        save_notes(request.user.username, notes)
        messages.success(request, 'Catatan berhasil dihapus!')
    return redirect('home')

def about_us(request):
    team_members = [
        {
            'name': 'Alfaridzy Awalrisan Polarit',
            'nim': '0110225090',
            'description': 'Bertanggung jawab dalam koordinasi tim dan merancang bagian back end.',
            'photo': 'https://iili.io/fSTUb24.md.jpg'
        },
        {
            'name': 'Dhanendra Putra Keywa',
            'nim': '0110225113',
            'description': 'Bertugas membuat PPT dengan canva dan merancang bagian front end.',
            'photo': 'https://iili.io/fSTUpv2.md.jpg'
        },
        {
            'name': 'Dirga Ananta Mahardika',
            'nim': '0110225101',
            'description': 'Bertugas membuat PPT dengan canva.',
            'photo': 'https://via.placeholder.com/150'
        },
        {
            'name': 'Nadia Calistha',
            'nim': '0110225091',
            'description': 'Bertugas membuat laporan dengan word.',
            'photo': 'https://iili.io/fSTUrkN.md.jpg'
        },
        {
            'name': 'Zihan Diva',
            'nim': '0110225069',
            'description': 'Bertugas membuat laporan dengan word.',
            'photo': 'https://iili.io/fSTUihX.md.jpg'
        },
    ]
    return render(request, 'about.html', {'team_members': team_members})

def gallery(request):
    photos = [
        {
            'title': 'Diskusi Tim',
            'description': 'Sesi brainstorming untuk fitur baru',
            'image': 'https://iili.io/fSuXdV2.md.jpg'
        },
        {
            'title': 'Coding Session',
            'description': 'Proses pengembangan backend',
            'image': 'https://iili.io/fSuXJol.md.jpg'
        },
        {
            'title': 'Code Review',
            'description': 'Review kode bersama tim',
            'image': 'https://iili.io/fSuX2PS.md.jpg'
        },
    ]
    return render(request, 'gallery.html', {'photos': photos})

def contact_whatsapp(request):
    if request.method == 'POST':
        nama = request.POST.get('nama', '')
        email = request.POST.get('email', '')
        pesan = request.POST.get('pesan', '')
        
        # Nomor WhatsApp tujuan (ganti dengan nomor Anda)
        # Format: 62 untuk Indonesia, tanpa + dan tanpa 0 di depan
        # Contoh: 6281234567890
        whatsapp_number = '6281234567890'  # GANTI DENGAN NOMOR WHATSAPP ANDA
        
        # Format pesan untuk WhatsApp
        pesan_whatsapp = f"""*Pesan dari Website MyNotepad*

*Nama:* {nama}
*Email:* {email}

*Pesan:*
{pesan}"""
        
        # Encode pesan untuk URL
        pesan_encoded = quote(pesan_whatsapp)
        
        # Buat URL WhatsApp
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={pesan_encoded}"
        
        # Redirect ke WhatsApp
        return redirect(whatsapp_url)
    
    # Jika bukan POST, redirect ke landing page
    return redirect('landing')