<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Kết quả tốt nghiệp</h2>
    @if ($result)
        <div class="bg-white p-8 rounded-lg shadow max-w-md text-center">
            <div class="text-gray-500 mb-2">GPA</div>
            <div class="text-5xl font-bold text-blue-600 mb-4">{{ number_format($result['gpa'], 2) }}</div>
            <div class="text-gray-500 mb-2">Xếp loại</div>
            <div class="text-3xl font-bold text-green-600">{{ $result['xep_loai'] }}</div>
        </div>
    @else
        <div class="bg-yellow-100 text-yellow-800 p-4 rounded-lg max-w-md">
            Bạn chưa được xét tốt nghiệp.
        </div>
    @endif
</div>
