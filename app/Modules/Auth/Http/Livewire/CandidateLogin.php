<?php

namespace App\Modules\Auth\Http\Livewire;

use App\Modules\Auth\Services\AuthService;
use App\Modules\TuyenSinh\Models\TKXetTuyen;
use Livewire\Component;

class CandidateLogin extends Component
{
    public string $email = '';
    public string $password = '';
    public bool $remember = false;

    protected array $rules = [
        'email' => 'required|email',
        'password' => 'required|min:6',
    ];

    protected array $messages = [
        'email.required' => 'Email là bắt buộc.',
        'email.email' => 'Email không hợp lệ.',
        'password.required' => 'Mật khẩu là bắt buộc.',
        'password.min' => 'Mật khẩu phải có ít nhất 6 ký tự.',
    ];

    public function login(AuthService $authService)
    {
        $this->validate();

        if ($authService->loginCandidate($this->email, $this->password)) {
            session()->regenerate();

            return redirect()->route('candidate.dashboard');
        }

        $this->addError('email', 'Email hoặc mật khẩu không đúng.');
    }

    public function render()
    {
        return view('livewire.auth.candidate-login')
            ->extends('layouts.app')
            ->section('content');
    }
}
