<?php

namespace App\Modules\Auth\Http\Livewire;

use App\Modules\TuyenSinh\Models\TKXetTuyen;
use App\Modules\TuyenSinh\Services\TuyenSinhService;
use Livewire\Component;

class CandidateRegister extends Component
{
    public string $email = '';
    public string $password = '';
    public string $password_confirmation = '';
    public string $hoTen = '';
    public string $cccd = '';
    public string $sdt = '';

    protected array $rules = [
        'email' => 'required|email|unique:tk_xet_tuyen,Email',
        'password' => 'required|min:6|confirmed',
        'hoTen' => 'required|string|max:100',
        'cccd'  => 'required|digits:10|unique:hso_xet_tuyen,CCCD',
        'sdt'   => 'required|digits:10|unique:hso_xet_tuyen,SDT',
    ];

    protected array $messages = [
        'email.required' => 'Email là bắt buộc.',
        'email.email' => 'Email không hợp lệ.',
        'email.unique' => 'Email đã được sử dụng.',
        'password.required' => 'Mật khẩu là bắt buộc.',
        'password.min' => 'Mật khẩu phải có ít nhất 6 ký tự.',
        'password.confirmed' => 'Xác nhận mật khẩu không khớp.',
        'hoTen.required' => 'Họ tên là bắt buộc.',
        'cccd.required' => 'CCCD là bắt buộc.',
        'cccd.digits' => 'CCCD phải có đúng 10 số.',
        'cccd.unique' => 'CCCD đã được sử dụng.',
        'sdt.required' => 'Số điện thoại là bắt buộc.',
        'sdt.digits' => 'Số điện thoại phải có đúng 10 số.',
        'sdt.unique' => 'Số điện thoại đã được sử dụng.',
    ];

    public function register(TuyenSinhService $service)
    {
        $this->validate();

        $tk = $service->registerCandidate([
            'Email'   => $this->email,
            'MatKhau' => $this->password,
        ]);

        $service->createProfile($tk->MaTK, [
            'HoTen' => $this->hoTen,
            'CCCD'  => $this->cccd,
            'SDT'   => $this->sdt,
        ]);

        session()->flash('success', 'Đăng ký thành công! Vui lòng đăng nhập.');
        return redirect()->route('candidate.login');
    }

    public function render()
    {
        return view('livewire.auth.candidate-register')
            ->extends('layouts.app')
            ->section('content');
    }
}
