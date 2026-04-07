<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Xét tốt nghiệp</h2>

    @if (session('success'))
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {{ session('success') }}
        </div>
    @endif

    <form wire:submit="xetTotNghiep" class="max-w-md bg-white p-6 rounded-lg shadow space-y-4">
        <div>
            <label class="block text-gray-700 font-medium mb-2">Chọn sinh viên</label>
            <select wire:model="maSV"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">-- Chọn sinh viên --</option>
                @foreach ($sinhViens as $sv)
                    <option value="{{ $sv['ma_sv'] }}">{{ $sv['ho_ten'] }} ({{ $sv['ma_sv'] }})</option>
                @endforeach
            </select>
            @error('maSV') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <button type="submit"
            class="w-full bg-purple-600 text-white py-3 px-4 rounded-lg hover:bg-purple-700 font-medium">
            Xét tốt nghiệp
        </button>
    </form>
</div>
