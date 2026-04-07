<?php

namespace App\Modules\Auth\Http\Livewire;

use App\Modules\SinhVien\Models\SinhVien;
use Livewire\Component;

class StudentLogin extends Component
{
    public string $maSV = '';
    public string $password = '';
    public bool $remember = false;

    protected array $rules = [
        'maSV' => 'required|string',
        'password' => 'required|min:6',
    ];

    protected array $messages = [
        'maSV.required' => 'Mã sinh viên là bắt buộc.',
        'password.required' => 'Mật khẩu là bắt buộc.',
        'password.min' => 'Mật khẩu phải có ít nhất 6 ký tự.',
    ];

    public function login()
    {
        $this->validate();

        if (\Illuminate\Support\Facades\Auth::guard('student')->attempt(['MaSV' => $this->maSV, 'password' => $this->password], $this->remember)) {
            session()->regenerate();
            return redirect()->route('student.dashboard');
        }

        $this->addError('maSV', 'Mã sinh viên hoặc mật khẩu không đúng.');
    }

    public function render()
    {
        return view('livewire.auth.student-login')
            ->extends('layouts.app')
            ->section('content');
    }
}
