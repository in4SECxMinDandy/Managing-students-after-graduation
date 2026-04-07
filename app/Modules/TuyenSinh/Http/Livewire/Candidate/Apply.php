<?php

namespace App\Modules\TuyenSinh\Http\Livewire\Candidate;

use App\Modules\Nganh\Models\Nganh;
use App\Modules\TuyenSinh\Services\TuyenSinhService;
use Livewire\Component;

class Apply extends Component
{
    public string $maNganh = '';
    public string $phuongThuc = '';
    public string $diem = '';
    public array $nganhs = [];

    protected array $rules = [
        'maNganh' => 'required|string',
        'phuongThuc' => 'required|string|max:100',
        'diem' => 'required|numeric|min:0|max:30',
    ];

    protected array $messages = [
        'maNganh.required' => 'Vui lòng chọn ngành.',
        'phuongThuc.required' => 'Phương thức xét tuyển là bắt buộc.',
        'diem.required' => 'Điểm là bắt buộc.',
        'diem.numeric' => 'Điểm phải là số.',
        'diem.min' => 'Điểm không được nhỏ hơn 0.',
        'diem.max' => 'Điểm không được lớn hơn 30.',
    ];

    public function mount()
    {
        $this->nganhs = Nganh::with('khoa')->get()->toArray();
    }

    public function submit(TuyenSinhService $service)
    {
        $this->validate();

        $user = auth()->guard('candidate')->user();
        $hso = $user->hsoXetTuyen->first();

        if (!$hso) {
            $this->addError('maNganh', 'Bạn cần hoàn thành hồ sơ trước.');
            return;
        }

        $service->submitApplication($hso->MaHSO, [
            'MaNganh'    => $this->maNganh,
            'PhuongThuc' => $this->phuongThuc,
            'Diem'       => $this->diem,
        ]);

        session()->flash('success', 'Nộp hồ sơ xét tuyển thành công!');
        return redirect()->route('candidate.status');
    }

    public function render()
    {
        return view('livewire.tuyen-sinh.candidate.apply')
            ->extends('layouts.app')
            ->section('content');
    }
}
