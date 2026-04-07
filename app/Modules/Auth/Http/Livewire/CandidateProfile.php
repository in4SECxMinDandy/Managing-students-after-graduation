<?php

namespace App\Modules\Auth\Http\Livewire;

use App\Modules\Auth\Services\AuthService;
use App\Modules\TuyenSinh\Models\HSOXetTuyen;
use Livewire\Component;

class CandidateProfile extends Component
{
    public ?object $candidate = null;

    public ?object $hso = null;

    public function mount(AuthService $authService): void
    {
        $this->candidate = $authService->currentUser();
        if ($this->candidate) {
            $this->hso = HSOXetTuyen::where('MaTK', $this->candidate->MaTK)->first();
        }
    }

    public function render()
    {
        return view('livewire.auth.candidate-profile')
            ->extends('layouts.app')
            ->section('content');
    }
}
