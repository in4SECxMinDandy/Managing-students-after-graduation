<?php

namespace App\Modules\TuyenSinh\Http\Livewire\Candidate;

use App\Modules\TuyenSinh\Models\PTXetTuyen;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class Status extends Component
{
    public array $applications = [];

    public function mount()
    {
        $user = Auth::guard('candidate')->user();
        $hso = $user->hsoXetTuyen->first();

        if ($hso) {
            $this->applications = PTXetTuyen::with('nghanh')
                ->where('MaHSO', $hso->MaHSO)
                ->get()
                ->toArray();
        }
    }

    public function render()
    {
        return view('livewire.tuyen-sinh.candidate.status')
            ->extends('layouts.app')
            ->section('content');
    }
}
