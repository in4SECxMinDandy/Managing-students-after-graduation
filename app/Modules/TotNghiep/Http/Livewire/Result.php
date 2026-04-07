<?php

namespace App\Modules\TotNghiep\Http\Livewire;

use App\Modules\TotNghiep\Services\TotNghiepService;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class Result extends Component
{
    public ?array $result = null;

    public function mount(TotNghiepService $service)
    {
        $user = Auth::guard('student')->user();
        $this->result = $service->getKetQua($user->MaSV)?->toArray();
    }

    public function render()
    {
        return view('livewire.tot-nghiep.result')
            ->extends('layouts.app')
            ->section('content');
    }
}
