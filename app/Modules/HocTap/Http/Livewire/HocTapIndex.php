<?php

namespace App\Modules\HocTap\Http\Livewire;

use App\Modules\HocTap\Models\KQHocTap;
use App\Modules\HocTap\Services\HocTapService;
use App\Modules\MonHoc\Models\MonHoc;
use App\Modules\SinhVien\Models\SinhVien;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;

class HocTapIndex extends Component
{
    public array $sinhViens = [];
    public array $monHocs = [];
    public string $maSV = '';
    public string $maMH = '';
    public string $diem = '';

    public function mount()
    {
        $this->sinhViens = SinhVien::all()->toArray();
        $this->monHocs = MonHoc::all()->toArray();
    }

    protected array $rules = [
        'maSV' => 'required|string',
        'maMH' => 'required|string',
        'diem' => 'required|numeric|min:0|max:10',
    ];

    protected array $messages = [
        'maSV.required' => 'Vui lòng chọn sinh viên.',
        'maMH.required' => 'Vui lòng chọn môn học.',
        'diem.required' => 'Điểm là bắt buộc.',
        'diem.numeric' => 'Điểm phải là số.',
        'diem.min' => 'Điểm không được nhỏ hơn 0.',
        'diem.max' => 'Điểm không được lớn hơn 10.',
    ];

    public function saveDiem(HocTapService $service)
    {
        $this->validate();
        $service->inputDiem($this->maSV, $this->maMH, (float) $this->diem);
        session()->flash('success', 'Lưu điểm thành công!');
        $this->reset(['maSV', 'maMH', 'diem']);
    }

    public function render()
    {
        return view('livewire.hoc-tap.index')
            ->extends('layouts.app')
            ->section('content');
    }
}
