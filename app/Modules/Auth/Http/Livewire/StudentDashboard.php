<?php

namespace App\Modules\Auth\Http\Livewire;

use App\Modules\Auth\Services\AuthService;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class StudentDashboard extends Component
{
    public ?object $student = null;

    public function mount(AuthService $authService)
    {
        $this->student = $authService->currentUser();
    }

    public function render()
    {
        return view('livewire.auth.student-dashboard')
            ->extends('layouts.app')
            ->section('content');
    }
}
