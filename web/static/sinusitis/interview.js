(function () {
    const chat = document.getElementById('chat');
    const controls = document.getElementById('controls');
    let answers = {};

    function appendBot(text) {
        const el = document.createElement('div');
        el.className = 'flex items-start';
        el.innerHTML = `
      <div class="w-9 h-9 rounded-full bg-cyan-100 text-cyan-700 flex items-center justify-center mr-3">
        <i class="fas fa-stethoscope"></i>
      </div>
      <div class="bg-slate-100 rounded-2xl px-4 py-3 text-slate-800 max-w-[80%]">${text}</div>
    `;
        chat.appendChild(el);
        chat.scrollTop = chat.scrollHeight;
    }

    function appendUser(text) {
        const el = document.createElement('div');
        el.className = 'flex items-start justify-end';
        el.innerHTML = `
      <div class="bg-cyan-600 text-white rounded-2xl px-4 py-3 max-w-[80%]">${text}</div>
    `;
        chat.appendChild(el);
        chat.scrollTop = chat.scrollHeight;
    }

    function renderControls(q) {
        controls.innerHTML = '';
        if (!q) { return; }

        if (q.type === 'boolean') {
            controls.innerHTML = `
        <div class="flex gap-3">
          <button id="btnYes" class="px-6 py-3 bg-cyan-600 text-white rounded-lg font-semibold hover:bg-cyan-700">Có</button>
          <button id="btnNo" class="px-6 py-3 bg-slate-200 text-slate-700 rounded-lg font-semibold hover:bg-slate-300">Không</button>
        </div>
      `;
            document.getElementById('btnYes').onclick = () => submitAnswer(q, true, 'Có');
            document.getElementById('btnNo').onclick = () => submitAnswer(q, false, 'Không');
        }
        else if (q.type === 'number') {
            controls.innerHTML = `
        <div class="flex items-center gap-3">
          <input type="number" id="numInput" class="px-4 py-2 border rounded-lg" placeholder="Nhập số" min="${q.min ?? ''}" max="${q.max ?? ''}" step="${q.step ?? 1}" />
          <button id="btnOk" class="px-6 py-2 bg-cyan-600 text-white rounded-lg font-semibold hover:bg-cyan-700">Gửi</button>
        </div>
      `;
            document.getElementById('btnOk').onclick = () => {
                const v = document.getElementById('numInput').value;
                if (v === '') return;
                submitAnswer(q, Number(v), String(v));
            };
        }
        else if (q.type === 'radio' && Array.isArray(q.options)) {
            const opts = q.options.map((op, i) => `
        <label class="flex items-center p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100">
          <input type="radio" name="opt" value="${op}" ${i === 0 ? 'checked' : ''} class="w-4 h-4 text-cyan-600" />
          <span class="ml-3 text-sm text-slate-700">${op}</span>
        </label>`).join('');
            controls.innerHTML = `
        <div class="space-y-2 mb-2">${opts}</div>
        <button id="btnOk" class="px-6 py-2 bg-cyan-600 text-white rounded-lg font-semibold hover:bg-cyan-700">Gửi</button>
      `;
            document.getElementById('btnOk').onclick = () => {
                const picked = document.querySelector('input[name="opt"]:checked');
                if (!picked) return;
                submitAnswer(q, picked.value, picked.value);
            };
        }
    }

    async function fetchNext() {
        const res = await fetch('/sinusitis/api/next_question', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers })
        });
        const data = await res.json();

        if (!data.ok) {
            appendBot('Xin lỗi, hiện tại hệ thống chưa đủ dữ liệu để đưa ra nhận định an toàn. Bạn nên trao đổi trực tiếp với bác sĩ để được thăm khám đầy đủ hơn.');
            return;
        }

        if (data.done) {
            appendBot(`Dựa trên các thông tin bạn cung cấp, mình đã tổng hợp được một kết luận sơ bộ: <strong>${data.summary.label}</strong>.`);
            const el = document.createElement('div');
            el.className = 'mt-4';
            el.innerHTML = `<a href="${data.result_url}" class="px-6 py-3 bg-cyan-600 text-white rounded-lg font-semibold hover:bg-cyan-700">Xem giải thích chi tiết và khuyến nghị như bác sĩ tư vấn</a>`;
            controls.innerHTML = '';
            controls.appendChild(el);
            return;
        }

        appendBot(data.question.label);
        renderControls(data.question);
    }

    function submitAnswer(q, value, rendered) {
        appendUser(rendered);
        answers[q.variable] = value;
        fetchNext();
    }

    // Bắt đầu phỏng vấn giống quy trình bác sĩ: hỏi từng ý quan trọng, không lan man
    fetchNext();
})();
