<?php

namespace App\Modules\Auth\Services;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class AuthService
{
    public function loginCandidate(string $email, string $password): bool
    {
        return Auth::guard('candidate')->attempt([
            'Email'    => $email,
            'password' => $password,
        ]);
    }

    public function loginStudent(string $maSV, string $password): bool
    {
        return Auth::guard('student')->attempt([
            'MaSV'     => $maSV,
            'password' => $password,
        ]);
    }

    public function loginAdmin(string $tenDN, string $password): bool
    {
        return Auth::guard('admin')->attempt([
            'TenDN'    => $tenDN,
            'password' => $password,
        ]);
    }

    public function logout(): void
    {
        if (Auth::guard('candidate')->check()) {
            Auth::guard('candidate')->logout();
        } elseif (Auth::guard('student')->check()) {
            Auth::guard('student')->logout();
        } elseif (Auth::guard('admin')->check()) {
            Auth::guard('admin')->logout();
        }
        session()->invalidate();
        session()->regenerateToken();
    }

    public function currentUser(): mixed
    {
        if (Auth::guard('candidate')->check()) {
            return Auth::guard('candidate')->user();
        }
        if (Auth::guard('student')->check()) {
            return Auth::guard('student')->user();
        }
        if (Auth::guard('admin')->check()) {
            return Auth::guard('admin')->user();
        }
        return null;
    }

    public function currentGuard(): ?string
    {
        foreach (['candidate', 'student', 'admin'] as $guard) {
            if (Auth::guard($guard)->check()) {
                return $guard;
            }
        }
        return null;
    }
}
