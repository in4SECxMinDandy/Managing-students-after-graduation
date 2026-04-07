<?php

namespace App\Modules\TotNghiep\Http\Livewire;

use App\Modules\SinhVien\Models\SinhVien;
use App\Modules\TotNghiep\Services\TotNghiepService;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class TotNghiepIndex extends Component
{
    public array $sinhViens = [];
    public string $maSV = '';

    public function mount()
    {
        $this->sinhViens = SinhVien::all()->toArray();
    }

    protected array $rules = [
        'maSV' => 'required|string|exists:sinh_vien,MaSV',
    ];

    protected array $messages = [
        'maSV.required' => 'Vui lòng chọn sinh viên.',
        'maSV.exists' => 'Sinh viên không tồn tại.',
    ];

    public function xetTotNghiep(TotNghiepService $service)
    {
        $this->validate();
        $result = $service->xetTotNghiep($this->maSV);
        session()->flash('success', "Xét tốt nghiệp thành công! GPA: {$result->GPA} - {$result->XepLoai}");
        $this->reset('maSV');
    }

    public function render()
    {
        return view('livewire.tot-nghiep.index')
            ->extends('layouts.app')
            ->section('content');
    }
}
