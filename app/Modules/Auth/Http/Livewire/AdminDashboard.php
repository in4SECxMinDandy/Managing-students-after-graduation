<?php

namespace App\Modules\Auth\Http\Livewire;

use App\Modules\Auth\Services\AuthService;
use Livewire\Component;

class AdminDashboard extends Component
{
    public ?object $admin = null;

    public function mount(AuthService $authService)
    {
        $this->admin = $authService->currentUser();
    }

    public function render()
    {
        return view('livewire.auth.admin-dashboard')
            ->extends('layouts.app')
            ->section('content');
    }
}
