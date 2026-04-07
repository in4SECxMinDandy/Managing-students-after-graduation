<?php

namespace App\Modules\Auth\Http\Livewire;

use App\Modules\QuanTri\Models\QuanTri;
use Livewire\Component;

class AdminLogin extends Component
{
    public string $tenDN = '';
    public string $password = '';
    public bool $remember = false;

    protected array $rules = [
        'tenDN' => 'required|string',
        'password' => 'required|min:6',
    ];

    protected array $messages = [
        'tenDN.required' => 'Tên đăng nhập là bắt buộc.',
        'password.required' => 'Mật khẩu là bắt buộc.',
        'password.min' => 'Mật khẩu phải có ít nhất 6 ký tự.',
    ];

    public function login()
    {
        $this->validate();

        if (\Illuminate\Support\Facades\Auth::guard('admin')->attempt(['TenDN' => $this->tenDN, 'password' => $this->password], $this->remember)) {
            session()->regenerate();
            return redirect()->route('admin.dashboard');
        }

        $this->addError('tenDN', 'Tên đăng nhập hoặc mật khẩu không đúng.');
    }

    public function render()
    {
        return view('livewire.auth.admin-login')
            ->extends('layouts.app')
            ->section('content');
    }
}
