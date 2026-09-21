from pathlib import Path

path = Path('/home/ubuntu/RTM/index.html')
html = path.read_text()

section = r'''
        <!-- ==================== VIMAX AI VIDEO DEMO ==================== -->
        <section class="lg:col-span-12 glass-panel rounded-3xl p-5 md:p-7 border border-cyan-500/30 mt-2">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-5">
                <div>
                    <p class="text-[10px] uppercase tracking-[0.25em] text-cyan-300 font-bold">ViMax / RTM Integration</p>
                    <h2 class="text-2xl md:text-3xl font-black mt-1">AI Video Studio Demo</h2>
                    <p class="text-sm text-slate-300 mt-2 max-w-2xl">ViMax orchestration + Gemini Veo render pipeline ဖြင့် ထုတ်ထားသော demo။ ဒီ panel က generated MP4 ကို preview နှင့် download လုပ်နိုင်ရန် ထည့်ထားခြင်းဖြစ်သည်။</p>
                </div>
                <span class="inline-flex items-center gap-2 px-3 py-2 rounded-full bg-emerald-500/15 border border-emerald-400/30 text-emerald-300 text-xs font-bold"><span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> ViMax Connected</span>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
                <div class="lg:col-span-8 rounded-2xl overflow-hidden bg-black border border-slate-700 shadow-2xl">
                    <video id="vimaxDemoVideo" class="w-full aspect-video object-cover" controls playsinline preload="metadata">
                        <source src="assets/vimax/rtm_vimax_demo.mp4" type="video/mp4">
                        Your browser does not support HTML5 video.
                    </video>
                </div>
                <div class="lg:col-span-4 space-y-3">
                    <div class="rounded-2xl bg-slate-900/70 border border-slate-700 p-4">
                        <p class="text-xs uppercase tracking-widest text-slate-400 font-bold">Demo Prompt</p>
                        <p class="text-sm text-slate-200 mt-2 leading-relaxed">“Cinematic documentary shot of a small solar-powered community workshop at sunrise…”</p>
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-center">
                        <div class="rounded-xl bg-slate-900/70 border border-slate-700 p-3"><p class="text-[10px] text-slate-400 uppercase">Model</p><p class="text-sm font-bold text-cyan-300 mt-1">Veo 3.1</p></div>
                        <div class="rounded-xl bg-slate-900/70 border border-slate-700 p-3"><p class="text-[10px] text-slate-400 uppercase">Format</p><p class="text-sm font-bold text-cyan-300 mt-1">16:9 / 8 sec</p></div>
                    </div>
                    <a href="assets/vimax/rtm_vimax_demo.mp4" download class="block text-center bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-black py-3 rounded-xl transition shadow-lg">⬇️ Demo Video Download</a>
                    <p class="text-[11px] text-slate-400 leading-relaxed">မှတ်ချက် — video generation ကို ViMax ရဲ့ official provider adapter နဲ့ server-side ပြုလုပ်ထားပြီး ဒီ UI က final artifact ကို local preview/download ပေးသည်။</p>
                </div>
            </div>
        </section>
'''

if 'id="vimaxDemoVideo"' not in html:
    html = html.replace('\n    </main>\n', '\n' + section + '\n    </main>\n', 1)
path.write_text(html)
print(f'patched {path}')
