<?php

use App\Http\Controllers\HomeController;
use App\Modules\Auth\Http\Livewire\AdminDashboard;
use App\Modules\Auth\Http\Livewire\AdminLogin;
use App\Modules\Auth\Http\Livewire\CandidateDashboard;
use App\Modules\Auth\Http\Livewire\CandidateLogin;
use App\Modules\Auth\Http\Livewire\CandidateProfile;
use App\Modules\Auth\Http\Livewire\CandidateRegister;
use App\Modules\Auth\Http\Livewire\StudentDashboard;
use App\Modules\Auth\Http\Livewire\StudentLogin;
use App\Modules\HocTap\Http\Livewire\HocTapIndex;
use App\Modules\HocTap\Http\Livewire\Transcript;
use App\Modules\Khoa\Http\Livewire\KhoaIndex;
use App\Modules\Lop\Http\Livewire\LopIndex;
use App\Modules\MonHoc\Http\Livewire\MonHocIndex;
use App\Modules\Nganh\Http\Livewire\NganhIndex;
use App\Modules\SinhVien\Http\Livewire\SinhVienIndex;
use App\Modules\SinhVien\Http\Livewire\SinhVienProfile;
use App\Modules\ThongBao\Http\Livewire\Admin\ThongBaoList as AdminThongBaoList;
use App\Modules\ThongBao\Http\Livewire\Student\ThongBaoList as StudentThongBaoList;
use App\Modules\TotNghiep\Http\Livewire\Result;
use App\Modules\TotNghiep\Http\Livewire\TotNghiepIndex;
use App\Modules\TuyenSinh\Http\Livewire\Admin\AdmissionList;
use App\Modules\TuyenSinh\Http\Livewire\Candidate\Apply;
use App\Modules\TuyenSinh\Http\Livewire\Candidate\Status;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Route;

Route::get('/', [HomeController::class, 'index'])->name('home');

Route::middleware('guest')->group(function () {
    Route::get('/candidate/login', CandidateLogin::class)->name('candidate.login');
    Route::get('/candidate/register', CandidateRegister::class)->name('candidate.register');
    Route::get('/student/login', StudentLogin::class)->name('student.login');
    Route::get('/admin/login', AdminLogin::class)->name('admin.login');
});

Route::middleware('auth.candidate')->prefix('candidate')->name('candidate.')->group(function () {
    Route::get('/dashboard', CandidateDashboard::class)->name('dashboard');
    Route::get('/profile', CandidateProfile::class)->name('profile');
    Route::get('/apply', Apply::class)->name('apply');
    Route::get('/status', Status::class)->name('status');
});

Route::middleware('auth.student')->prefix('student')->name('student.')->group(function () {
    Route::get('/dashboard', StudentDashboard::class)->name('dashboard');
    Route::get('/profile', SinhVienProfile::class)->name('profile');
    Route::get('/hoc-tap', Transcript::class)->name('hoc-tap');
    Route::get('/tot-nghiep', Result::class)->name('tot-nghiep');
    Route::get('/thong-bao', StudentThongBaoList::class)->name('thong-bao');
});

Route::middleware('auth.admin')->prefix('admin')->name('admin.')->group(function () {
    Route::get('/dashboard', AdminDashboard::class)->name('dashboard');
    Route::get('/khoa', KhoaIndex::class)->name('khoa');
    Route::get('/nganh', NganhIndex::class)->name('nganh');
    Route::get('/lop', LopIndex::class)->name('lop');
    Route::get('/mon-hoc', MonHocIndex::class)->name('mon-hoc');
    Route::get('/tuyen-sinh', AdmissionList::class)->name('tuyen-sinh');
    Route::get('/sinh-vien', SinhVienIndex::class)->name('sinh-vien');
    Route::get('/hoc-tap', HocTapIndex::class)->name('hoc-tap');
    Route::get('/tot-nghiep', TotNghiepIndex::class)->name('tot-nghiep');
    Route::get('/thong-bao', AdminThongBaoList::class)->name('thong-bao');
});

Route::post('/logout', function () {
    foreach (['admin', 'student', 'candidate'] as $guard) {
        if (Auth::guard($guard)->check()) {
            Auth::guard($guard)->logout();
        }
    }
    request()->session()->invalidate();
    request()->session()->regenerateToken();

    return redirect('/');
})->name('logout');
