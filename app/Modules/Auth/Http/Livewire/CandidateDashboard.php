<?php

namespace App\Modules\Auth\Http\Livewire;

use App\Modules\Auth\Services\AuthService;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class CandidateDashboard extends Component
{
    public ?object $candidate = null;

    public function mount(AuthService $authService)
    {
        $this->candidate = $authService->currentUser();
    }

    public function render()
    {
        return view('livewire.auth.candidate-dashboard')
            ->extends('layouts.app')
            ->section('content');
    }
}
