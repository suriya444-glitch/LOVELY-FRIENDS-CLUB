import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

nav_template = """    <!-- Navigation -->
    <nav class="glass-card sticky top-0 z-50 px-6 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-neonYellow flex items-center justify-center text-charcoal font-bebas text-2xl">LFC</div>
            <h1 class="text-2xl font-bebas tracking-wide text-white">LOVELY FRIENDS</h1>
        </div>
        <div class="hidden md:flex gap-8 font-inter font-semibold text-sm">
            <a href="index.html" class="nav-link{index_active}">HOME</a>
            <a href="stats.html" class="nav-link{stats_active}">MATCH STATS</a>
            <a href="gallery.html" class="nav-link{gallery_active}">GALLERY</a>
            <a href="squad.html" class="nav-link{squad_active}">SQUAD & INFO</a>
        </div>
        <!-- Mobile menu button -->
        <button id="mobile-menu-btn" class="md:hidden text-white focus:outline-none">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
        
        <!-- Mobile Menu -->
        <div id="mobile-menu" class="hidden absolute top-full left-0 w-full bg-charcoal border-t border-gray-800 flex-col font-inter font-semibold text-sm shadow-xl z-50">
            <a href="index.html" class="block px-6 py-4 border-b border-gray-800{index_active_mob}">HOME</a>
            <a href="stats.html" class="block px-6 py-4 border-b border-gray-800{stats_active_mob}">MATCH STATS</a>
            <a href="gallery.html" class="block px-6 py-4 border-b border-gray-800{gallery_active_mob}">GALLERY</a>
            <a href="squad.html" class="block px-6 py-4{squad_active_mob}">SQUAD & INFO</a>
        </div>
    </nav>"""

script_to_add = """
    <!-- Mobile Menu Script -->
    <script>
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if(mobileMenuBtn && mobileMenu) {
            mobileMenuBtn.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
                mobileMenu.classList.toggle('flex');
            });
        }
    </script>
"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to extract the original active state to preserve it better
    # or just use file matching
    is_index = file == 'index.html'
    is_stats = file == 'stats.html'
    is_gallery = file == 'gallery.html'
    is_squad = file == 'squad.html'
    
    if not (is_index or is_stats or is_gallery or is_squad):
        # Determine from existing content
        is_index = 'href="index.html" class="nav-link active"' in content
        is_stats = 'href="stats.html" class="nav-link active"' in content
        is_gallery = 'href="gallery.html" class="nav-link active"' in content
        is_squad = 'href="squad.html" class="nav-link active"' in content
    
    active_class = " active"
    text_white = " text-white text-neonYellow" # Just use text-white or neonYellow for active mobile link
    text_gray = " text-gray-300 hover:text-white"
    
    index_act = active_class if is_index else text_gray
    stats_act = active_class if is_stats else text_gray
    gallery_act = active_class if is_gallery else text_gray
    squad_act = active_class if is_squad else text_gray
    
    index_act_mob = text_white if is_index else text_gray
    stats_act_mob = text_white if is_stats else text_gray
    gallery_act_mob = text_white if is_gallery else text_gray
    squad_act_mob = text_white if is_squad else text_gray

    new_nav = nav_template.format(
        index_active=index_act,
        stats_active=stats_act,
        gallery_active=gallery_act,
        squad_active=squad_act,
        index_active_mob=index_act_mob,
        stats_active_mob=stats_act_mob,
        gallery_active_mob=gallery_act_mob,
        squad_active_mob=squad_act_mob
    )
    
    # Regex replace the nav
    new_content = re.sub(r'<!-- Navigation -->\s*<nav.*?</nav>', new_nav, content, flags=re.DOTALL)
    
    # Inject script before </body>
    if '<!-- Mobile Menu Script -->' not in new_content:
        new_content = re.sub(r'(</body>)', r'%s\n\1' % script_to_add, new_content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {file}")
