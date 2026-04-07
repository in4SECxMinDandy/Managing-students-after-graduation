<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Nộp hồ sơ xét tuyển</h2>

    @if (session('success'))
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {{ session('success') }}
        </div>
    @endif

    <form wire:submit="submit" class="max-w-lg bg-white p-6 rounded-lg shadow space-y-4">
        <div>
            <label class="block text-gray-700 font-medium mb-2">Chọn ngành</label>
            <select wire:model="maNganh"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">-- Chọn ngành --</option>
                @foreach ($nganhs as $nganh)
                    <option value="{{ $nganh['ma_nganh'] }}">
                        {{ $nganh['ten_nganh'] }} ({{ $nganh['khoa']['ten_khoa'] ?? '' }})
                    </option>
                @endforeach
            </select>
            @error('maNganh') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div>
            <label class="block text-gray-700 font-medium mb-2">Phương thức xét tuyển</label>
            <input type="text" wire:model="phuongThuc"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="VD: Điểm thi THPT Quốc gia">
            @error('phuongThuc') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div>
            <label class="block text-gray-700 font-medium mb-2">Điểm xét tuyển (0 - 30)</label>
            <input type="number" step="0.01" wire:model="diem"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="VD: 25.50">
            @error('diem') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <button type="submit"
            class="w-full bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 font-medium">
            Nộp hồ sơ
        </button>
    </form>
</div>
