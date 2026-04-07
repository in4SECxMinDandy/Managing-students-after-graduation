<?php

namespace App\Modules\HocTap\Http\Livewire;

use App\Modules\HocTap\Services\HocTapService;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class Transcript extends Component
{
    public array $transcript = [];
    public float $gpa = 0.00;

    public function mount(HocTapService $service)
    {
        $user = Auth::guard('student')->user();
        $this->transcript = $service->getTranscript($user->MaSV)->toArray();
        $this->gpa = $service->tinhGPA($user->MaSV);
    }

    public function render()
    {
        return view('livewire.hoc-tap.transcript')
            ->extends('layouts.app')
            ->section('content');
    }
}
