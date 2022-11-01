# Nikita Akimov interplanety@interplanety.org
# Alexander Reshetnyak

# version history
# 1.0.0. - release
# 1.0.1. - если строка поиска не поменялась, но пользователь кликнул на поле поиска а потом вне его - не производить поиск
# 1.0.2. - prefix и region в UI разбиты на равномерные части
# 1.0.3. - добавлен выпадающий список, prefix region откат разметки
# 1.0.4. - убраны некоторые пункты ui и переработан выпадающий список


import bpy
from bpy.props import StringProperty, BoolProperty, PointerProperty, EnumProperty
from bpy.types import PropertyGroup, WindowManager, Panel, Operator
from bpy.utils import register_class, unregister_class


bl_info = {
    'name': 'Youtube Search',
    'category': 'Search',
    'author': 'Nikita Akimov, Alexander Reshetnyak',
    'version': (1, 0, 4),
    'blender': (2, 91, 0),
    'location': 'Properties window - Render Properties tab',
    'wiki_url': '',
    'tracker_url': '',
    'description': 'Quick search on youtube'
}

# --- VARS ---

class YOUTUBE_SEARCH_vars(PropertyGroup):

    search: StringProperty(
        name='Search',
        default='',
        update=lambda self, context: self.on_update(context=context)
    )

    search_old: StringProperty(
        name='Search',
        default=''
    )

    prefix: StringProperty(
        name='Prefix',
        default='blender'
    )

    selector: EnumProperty(
        name='Sort by',
        items=[
            ('EMPTY', '', '', '', 0),
            ('CAISAhAB', 'Upload date', '', '', 1),
            ('CAASAhAB', 'Relevance', '', '', 2),
            ('CAMSAhAB', 'View count', '', '', 3),
            ('CAESAhAB', 'Rating', '', '', 4)
        ],
        default='EMPTY'
    )

    def on_update(self, context):
        if self.search_old != self.search:
            self.search_old = self.search
            bpy.ops.youtube_search.search(
                search=self.search,
                prefix=self.prefix
            )

# --- OPS ---

class YOUTUBE_SEARCH_OT_search(Operator):
    bl_idname = 'youtube_search.search'
    bl_label = 'Search'
    bl_description = 'Search on Youtube'

    search: StringProperty(
        default=''
    )

    prefix: StringProperty(
        default=''
    )

    def execute(self, context):
        # form url
        url_base = 'https://www.youtube.com/results?'
        url_vars = ''
        if self.search:
            url_vars += 'search_query='
            if self.prefix:
                url_vars += self.prefix.strip() + ' '
            url_vars += self.search.strip()
            if context.window_manager.youtube_search_vars.selector != 'EMPTY':
                url_vars += '&sp=' + context.window_manager.youtube_search_vars.selector
        url = url_base + url_vars

        bpy.ops.wm.url_open(
            'INVOKE_DEFAULT',
            url=url
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.window_manager.youtube_search_vars.search)

# --- UI ---

class YOUTUBE_SEARCH_PT_panel(Panel):
    bl_idname = 'YOUTUBE_SEARCH_PT_panel'
    bl_label = 'YouTube Search'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = 'Search'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        op_vars = context.window_manager.youtube_search_vars
        layout.prop(data=op_vars, property='prefix')
        # search field
        row = layout.row()
        row.prop(data=op_vars, property='search', text='')
        # search button
        op = row.operator('youtube_search.search', text='', icon='VIEWZOOM')
        op.search = op_vars.search
        op.prefix = op_vars.prefix
        # params
        layout.prop(data=op_vars, property='selector')


def register():
    register_class(YOUTUBE_SEARCH_vars)
    WindowManager.youtube_search_vars = PointerProperty(type=YOUTUBE_SEARCH_vars)
    register_class(YOUTUBE_SEARCH_OT_search)
    register_class(YOUTUBE_SEARCH_PT_panel)


def unregister():
    unregister_class(YOUTUBE_SEARCH_PT_panel)
    unregister_class(YOUTUBE_SEARCH_OT_search)
    del WindowManager.youtube_search_vars
    unregister_class(YOUTUBE_SEARCH_vars)


if __name__ == '__main__':
    register()
