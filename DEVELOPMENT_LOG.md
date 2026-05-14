# EventNow Development Log

本文件用于记录 EventNow 项目每一次代码更改后的新增功能、对应代码位置，以及 debug/更新内容。

记录格式：

```text
YYYY-MM-DD iterationN HH:MM:SS 时区：在 文件路径 中更新/新增 函数或模块，实现/修复 具体功能。
```

## 2026-05-09

- 2026-05-09 iteration1 23:03:00 AEST：在 `manage.py` 中新增 `main()` 函数，实现 Django 管理命令入口，用于后续运行 `runserver`、`migrate`、`check` 等命令。

- 2026-05-09 iteration1 23:03:00 AEST：在 `config/settings.py` 中新增项目基础配置，实现 `INSTALLED_APPS`、`MIDDLEWARE`、`TEMPLATES`、`DATABASES`、`STATIC_URL`、`STATICFILES_DIRS` 和 `STATIC_ROOT` 的初步配置。

- 2026-05-09 iteration1 23:03:00 AEST：在 `config/settings.py` 中新增 `load_dotenv(BASE_DIR / ".env")`，实现后续通过 `.env` 管理本地和部署环境配置的基础能力。

- 2026-05-09 iteration1 23:03:00 AEST：在 `config/settings.py` 中新增 `whitenoise.middleware.WhiteNoiseMiddleware`，为后续 Render 部署时提供静态文件支持。

- 2026-05-09 iteration1 23:03:00 AEST：在 `config/urls.py` 中新增项目级 URL routing，实现首页 `""`、`accounts/`、`events/`、`subscriptions/` 和 `admin/` 路由连接。

- 2026-05-09 iteration1 23:03:00 AEST：在 `config/urls.py` 中新增 `TemplateView.as_view(template_name="home.html")`，实现 EventNow 首页的基础页面展示。

- 2026-05-09 iteration1 23:03:00 AEST：在 `config/wsgi.py` 中新增 WSGI 配置，实现后续传统服务器部署入口。

- 2026-05-09 iteration1 23:03:00 AEST：在 `config/asgi.py` 中新增 ASGI 配置，实现后续异步服务器部署入口。

- 2026-05-09 iteration1 23:03:00 AEST：在 `accounts/views.py` 中新增 `login_view()` 函数，实现登录页面的 placeholder 渲染。

- 2026-05-09 iteration1 23:03:00 AEST：在 `accounts/views.py` 中新增 `register_view()` 函数，实现注册页面的 placeholder 渲染。

- 2026-05-09 iteration1 23:03:00 AEST：在 `accounts/views.py` 中新增 `logout_view()` 函数，实现退出登录页面的 placeholder 渲染，后续会接入 Django logout 逻辑。

- 2026-05-09 iteration1 23:03:00 AEST：在 `accounts/urls.py` 中新增 `urlpatterns`，实现 `login/`、`register/`、`logout/` 三个 accounts 路由。

- 2026-05-09 iteration1 23:03:00 AEST：在 `accounts/decorators.py` 中新增权限装饰器占位文件，为后续 `organiser_required`、`admin_required` 等角色检查做准备。

- 2026-05-09 iteration1 23:03:00 AEST：在 `events/views.py` 中新增 `event_list()` 函数，实现 event 列表页面的 placeholder 渲染。

- 2026-05-09 iteration1 23:03:00 AEST：在 `events/views.py` 中新增 `event_detail(request, event_id)` 函数，实现 event detail placeholder 页面，并向 template 传入 `event_id`。

- 2026-05-09 iteration1 23:03:00 AEST：在 `events/views.py` 中新增 `organiser_dashboard()` 函数，实现 organiser dashboard placeholder 页面。

- 2026-05-09 iteration1 23:03:00 AEST：在 `events/urls.py` 中新增 `urlpatterns`，实现 events app 的 event 列表、event 详情和 organiser dashboard 路由。

- 2026-05-09 iteration1 23:03:00 AEST：在 `subscriptions/views.py` 中新增 `subscription_list()` 函数，实现 subscription 列表页面的 placeholder 渲染。

- 2026-05-09 iteration1 23:03:00 AEST：在 `subscriptions/urls.py` 中新增 `urlpatterns`，实现 subscriptions app 的基础入口路由。

- 2026-05-09 iteration1 23:03:00 AEST：在 `templates/base.html` 中新增 Django template inheritance 基础结构，实现统一 header、navigation、main content、footer、`title` block 和 `content` block。

- 2026-05-09 iteration1 23:03:00 AEST：在 `templates/home.html` 中新增首页模板，实现 EventNow 标题、简介内容、Events 和 Register 入口按钮。

- 2026-05-09 iteration1 23:03:00 AEST：在 `templates/accounts/login.html` 中新增登录页面模板，实现继承 `base.html` 的 placeholder 页面。

- 2026-05-09 iteration1 23:03:00 AEST：在 `templates/accounts/register.html` 中新增注册页面模板，实现继承 `base.html` 的 placeholder 页面。

- 2026-05-09 iteration1 23:03:00 AEST：在 `templates/events/event_list.html` 中新增 event 列表模板，实现继承 `base.html` 的 placeholder 页面。

- 2026-05-09 iteration1 23:03:00 AEST：在 `templates/events/event_detail.html` 中新增 event 详情模板，实现显示 `event_id` 的 placeholder 页面。

- 2026-05-09 iteration1 23:03:00 AEST：在 `templates/events/organiser_dashboard.html` 中新增 organiser dashboard 模板，实现 organiser 管理入口 placeholder 页面。

- 2026-05-09 iteration1 23:03:00 AEST：在 `templates/subscriptions/subscription_list.html` 中新增 subscription 列表模板，实现 subscriptions app 的 placeholder 页面。

- 2026-05-09 iteration1 23:03:00 AEST：在 `static/css/main.css` 中新增基础样式，实现简洁现代的页面布局、导航、按钮、内容面板和 footer 样式。

- 2026-05-09 iteration1 23:03:00 AEST：在 `static/css/main.css` 中新增 `@media (max-width: 450px)` 响应式样式，实现移动端导航、按钮和内容布局适配。

- 2026-05-09 iteration1 23:03:00 AEST：在 `requirements.txt` 中新增 `Django`、`psycopg2-binary`、`gunicorn`、`whitenoise`、`python-dotenv`、`dj-database-url`，实现本地开发和后续部署的基础依赖记录。

- 2026-05-09 iteration1 23:03:00 AEST：在 `.env.example` 中新增 `SECRET_KEY`、`DEBUG`、`DATABASE_URL` 示例配置，实现后续环境变量配置参考。

- 2026-05-09 iteration1 23:03:00 AEST：在 `.gitignore` 中新增 `.env`、`__pycache__/`、`*.pyc`、`db.sqlite3`、`staticfiles/`、`.venv/`、`env/`、`media/`，避免提交本地环境、缓存、数据库和上传文件。

- 2026-05-09 iteration1 23:03:00 AEST：在 `README.md` 中新增项目简介、当前结构、本地运行步骤、app 职责、后续开发计划和测试账号说明。

- 2026-05-09 iteration1 23:06:00 AEST：对项目 Python 文件执行语法编译检查，确认 `accounts`、`events`、`subscriptions`、`config` 和 `manage.py` 没有语法错误。

- 2026-05-09 iteration1 23:06:00 AEST：在 `.gitignore` 中新增 `.DS_Store`，修复 macOS 系统文件可能被误提交的问题。

- 2026-05-09 iteration1 23:46:00 AEST：新增项目本地虚拟环境 `.venv`，用于隔离 EventNow 项目的 Python 依赖。

- 2026-05-09 iteration1 23:47:00 AEST：根据 `requirements.txt` 安装 Django 与部署相关依赖，实现本地运行 Django 项目的环境准备。

- 2026-05-09 iteration1 23:47:00 AEST：运行 `.venv/bin/python -m django --version`，确认当前 Django 版本为 `4.2.30`。

- 2026-05-09 iteration1 23:47:00 AEST：运行 `.venv/bin/python manage.py check`，确认 Django 项目配置检查通过，结果为 `System check identified no issues (0 silenced).`

- 2026-05-09 iteration1 23:48:08 AEST：新增 `DEVELOPMENT_LOG.md`，用于记录后续每一次代码更新、函数变更、新功能和 debug 内容。

## 2026-05-10

- 2026-05-10 iteration2 22:47:34 AEST：在 `accounts/models.py` 中新增 `UserProfile` model，实现基于 Django 内置 `User` 的角色扩展，包含 `attendee`、`organiser`、`admin` 三种 `TextChoices` 角色。

- 2026-05-10 iteration2 22:47:34 AEST：在 `accounts/admin.py` 中新增 `UserProfileAdmin`，实现用户角色资料的 admin 管理，支持 `list_display`、`list_filter`、`search_fields` 和 `ordering`。

- 2026-05-10 iteration2 22:47:34 AEST：在 `subscriptions/models.py` 中新增 `Organisation` model，实现 organiser 所属组织信息，包含 owner、status、created_at 和 updated_at。

- 2026-05-10 iteration2 22:47:34 AEST：在 `subscriptions/models.py` 中新增 `Subscription` model，实现 organisation 的 SaaS subscription 记录；subscription 持有 organisation 外键，方便保存订阅历史。

- 2026-05-10 iteration2 22:47:34 AEST：在 `subscriptions/admin.py` 中新增 `OrganisationAdmin` 和 `SubscriptionAdmin`，实现 organisation 与 subscription 的基础后台管理。

- 2026-05-10 iteration2 22:47:34 AEST：在 `subscriptions/admin.py` 中新增 `archive_selected_subscriptions()` admin action，实现将选中的 subscriptions 标记为 `archived`，避免真正删除数据。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/models.py` 中新增 `Category` model，实现 event 分类管理。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/models.py` 中新增 `Venue` model，实现 event 场地、地址、城市和房间信息管理。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/models.py` 中新增 `Event` model，实现核心活动数据结构，包含 organisation、organiser、category、venue、title、description、start_datetime、end_datetime、capacity、price 和 status。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/models.py` 中新增 `Event.clean()`，实现基础 validation：活动结束时间不能早于开始时间，capacity 必须大于 0。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/models.py` 中新增 `Session` model，实现 event 下的 session 数据结构，包含 start_datetime、end_datetime 和 capacity，方便后续做 session capacity tracking。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/models.py` 中新增 `Session.clean()`，实现基础 validation：session 结束时间不能早于开始时间，capacity 必须大于 0。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/models.py` 中新增 `Registration` model，实现用户对 event 的报名记录，并通过 unique constraint 避免同一个 user 重复注册同一个 event。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/models.py` 中新增 `SessionSelection` model，实现报名后选择 session 的记录，并通过 unique constraint 避免重复选择同一个 session。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/models.py` 中新增 `SavedEvent` model，实现用户保存 event 的功能，并通过 unique constraint 避免重复保存。

- 2026-05-10 iteration2 22:47:34 AEST：在 `events/admin.py` 中新增 `CategoryAdmin`、`VenueAdmin`、`EventAdmin`、`SessionAdmin`、`RegistrationAdmin`、`SessionSelectionAdmin` 和 `SavedEventAdmin`，实现所有 events 相关 models 的基础后台管理。

- 2026-05-10 iteration2 22:47:34 AEST：新增 `accounts/migrations/__init__.py`、`events/migrations/__init__.py` 和 `subscriptions/migrations/__init__.py`，修复 Django `makemigrations` 无法识别新增 models 的问题。

- 2026-05-10 iteration2 22:47:34 AEST：运行 `.venv/bin/python manage.py check`，确认新增 models 和 admin 配置通过 Django 系统检查。

- 2026-05-10 iteration2 22:47:34 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认 Django 能识别本次新增 models，并会生成 `accounts`、`subscriptions` 和 `events` 的初始 migration 文件。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/models.py` 中更新 `UserProfile.user` 的 `related_name` 为 `userprofile`，方便权限判断统一使用 `user.userprofile.role`。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/forms.py` 中新增 `RegisterForm`，基于 Django `UserCreationForm` 实现 username、email、password1、password2 和 role 注册字段。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/forms.py` 中更新 `RegisterForm.save()`，实现注册时保存 Django `User`，并创建或更新对应 `UserProfile`。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/forms.py` 中限制普通注册用户只能选择 `attendee` 或 `organiser`，admin role 只能由平台管理员通过 Django Admin 分配。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/decorators.py` 中新增 `get_user_role()`，实现安全读取 `user.userprofile.role`，如果用户没有 `UserProfile` 则默认作为 attendee。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/decorators.py` 中新增 `organiser_required()`，实现 organiser、admin 或 superuser 才能访问 organiser 页面，否则提示错误并跳转到 event list。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/decorators.py` 中新增 `admin_required()`，实现 admin role 或 superuser 才能访问 admin-only 页面，否则提示错误并跳转到 home。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/views.py` 中更新 `register_view()`，实现 GET 显示注册表单、POST 验证保存用户、注册成功后自动 login，并按角色跳转。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/views.py` 中更新 `login_view()`，实现基于 `AuthenticationForm` 的真实登录逻辑、失败提示和已登录用户自动跳转。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/views.py` 中更新 `logout_view()`，实现真实 logout、成功 message 和跳转到 home。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/views.py` 中新增 `dashboard_redirect_view()`，实现基于角色的跳转：organiser 到 organiser dashboard，admin/superuser 到 subscription list，attendee 到 event list。

- 2026-05-10 iteration3 22:56:42 AEST：在 `accounts/urls.py` 中新增 `dashboard/` 路由，连接 `dashboard_redirect_view()` 作为登录和注册后的统一跳转入口。

- 2026-05-10 iteration3 22:56:42 AEST：在 `events/views.py` 中为 `organiser_dashboard()` 添加 `login_required` 和 `organiser_required`，实现 organiser/admin 页面权限保护。

- 2026-05-10 iteration3 22:56:42 AEST：在 `subscriptions/views.py` 中为 `subscription_list()` 添加 `login_required` 和 `admin_required`，实现 subscription 管理页面权限保护。

- 2026-05-10 iteration3 22:56:42 AEST：在 `templates/accounts/login.html` 中更新登录页面，显示 Django 登录表单、CSRF token、错误信息、submit button 和 register 链接。

- 2026-05-10 iteration3 22:56:42 AEST：在 `templates/accounts/register.html` 中更新注册页面，显示 username、email、password1、password2、role 字段，并提示 admin account 必须由平台管理员分配。

- 2026-05-10 iteration3 22:56:42 AEST：在 `templates/base.html` 中更新导航栏，未登录用户显示 Login/Register，已登录用户显示 username/Logout，并根据角色显示 Organiser Dashboard 和 Subscriptions。

- 2026-05-10 iteration3 22:56:42 AEST：在 `templates/base.html` 中新增 Django messages 显示区域，实现登录、注册、退出和权限错误提示。

- 2026-05-10 iteration3 22:56:42 AEST：在 `static/css/main.css` 中新增 auth form、message 和 nav user 样式，使 login/register 页面保持清晰可读。

- 2026-05-10 iteration3 22:56:42 AEST：新增 `accounts/migrations/0002_alter_userprofile_user.py`，记录 `UserProfile.user` 的 related_name 更新，保持 model 和 migration 一致。

- 2026-05-10 iteration3 22:56:42 AEST：运行 `.venv/bin/python manage.py check`，确认第三阶段 authentication、role-based access control 和 templates 配置通过 Django 系统检查。

- 2026-05-10 iteration3 22:56:42 AEST：运行 Django test client 检查 `/`、`/accounts/login/`、`/accounts/register/`、`/events/` 返回 200，未登录访问 organiser dashboard 和 subscriptions 页面返回 302 并跳转到 login。

- 2026-05-10 iteration3 22:56:42 AEST：第三阶段完成后，下一步建议开发 Event CRUD：让 organiser 可以创建、编辑、查看和 archive 自己 organisation 下的 events。

## 2026-05-11

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/forms.py` 中新增 `EventForm`，基于 `ModelForm` 实现 organiser 创建和编辑 event 的表单，字段包含 organisation、category、venue、title、description、start_datetime、end_datetime、capacity、price 和 status。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/forms.py` 中为 `start_datetime` 和 `end_datetime` 设置 `datetime-local` widget，方便浏览器显示日期时间输入框。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/forms.py` 中让 `EventForm` 接收当前 user，并限制普通 organiser 只能选择自己拥有的 organisation，避免为其他 organiser 的 organisation 创建 event。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/views.py` 中新增 `can_manage_event()`，实现 organiser ownership protection：普通 organiser 只能管理自己创建的 event，admin role 和 superuser 可以管理所有 event。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/views.py` 中更新 `event_list()`，实现公开 event list，只显示 `published` events，并支持 keyword 搜索和 category 过滤。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/views.py` 中更新 `event_detail()`，实现公开 event 详情；普通用户只能查看 published event，event owner、admin 和 superuser 可以查看 draft、pending 或 archived event。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/views.py` 中新增 `organiser_event_list()`，实现 organiser event management 列表；普通 organiser 只看到自己创建的 events，admin/superuser 可以看到所有 events，并支持 status 过滤。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/views.py` 中新增 `event_create()`，实现 organiser 创建 event；organiser 字段不从表单选择，而是在 view 中自动设置为 `request.user`。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/views.py` 中新增 `event_edit()`，实现 organiser 编辑 event，并在保存前检查当前用户是否有权限管理该 event。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/views.py` 中新增 `event_archive()`，实现 event archive confirmation 和 POST archive；archive 不删除数据，只把 `status` 更新为 `archived`。

- 2026-05-11 iteration4 10:39:41 AEST：在 `events/urls.py` 中新增 organiser Event CRUD 路由，包括 `organiser_event_list`、`event_create`、`event_edit` 和 `event_archive`。

- 2026-05-11 iteration4 10:39:41 AEST：在 `templates/events/organiser_dashboard.html` 中更新 organiser workflow 入口，新增 Manage Events、Create Event、Manage Sessions Coming soon 和 View Registrations Coming soon。

- 2026-05-11 iteration4 10:39:41 AEST：新增 `templates/events/organiser_event_list.html`，实现 organiser event table，显示 title、status badge、start_datetime、capacity、price 和 View/Edit/Archive 操作。

- 2026-05-11 iteration4 10:39:41 AEST：新增 `templates/events/event_form.html`，实现 create/edit 共用表单页面，包含 CSRF token、form errors、Save 和 Cancel 按钮。

- 2026-05-11 iteration4 10:39:41 AEST：新增 `templates/events/event_confirm_archive.html`，实现 archive 确认页，并说明 archive 不会永久删除，只会从 public list 中隐藏。

- 2026-05-11 iteration4 10:39:41 AEST：在 `templates/events/event_list.html` 中更新 public event list，使用 card 展示 published events，并显示搜索框、category filter 和 empty state。

- 2026-05-11 iteration4 10:39:41 AEST：在 `templates/events/event_detail.html` 中更新 event detail 页面，显示 title、description、category、venue、time、capacity、price、status 和 later registration 提示。

- 2026-05-11 iteration4 10:39:41 AEST：在 `static/css/main.css` 中新增 dashboard card、event card、filter bar、data table、status badge、danger button、detail list 和 mobile responsive 样式。

- 2026-05-11 iteration4 10:39:41 AEST：运行 `.venv/bin/python manage.py check`，确认第四阶段 Event CRUD、权限保护、templates 和 urls 配置通过 Django 系统检查。

- 2026-05-11 iteration4 10:39:41 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认第四阶段没有新增数据库字段，不需要新的 migration。

- 2026-05-11 iteration4 10:39:41 AEST：运行 Django test client 检查 `/events/` 返回 200，未登录访问 organiser event list 和 create event 页面返回 302 并跳转到 login。

- 2026-05-11 iteration4 10:39:41 AEST：第四阶段完成后，下一步建议开发 Session CRUD：让 organiser 可以为自己的 event 创建、编辑和 archive sessions，并开始做 session capacity tracking。

- 2026-05-11 iteration4 10:41:57 AEST：在 `DEVELOPMENT_LOG.md` 中统一更新日志格式，为当前和后续记录添加 `iterationN` 前缀，方便区分每一次开发迭代。

- 2026-05-11 iteration5 10:49:30 AEST：在 `events/models.py` 中更新 `Event.clean()`，修复 price 可以为负数的问题；现在 price 必须大于等于 0，免费活动统一使用 0。

- 2026-05-11 iteration5 10:49:30 AEST：在 `events/models.py` 中加强 `Event.clean()` 的时间验证，要求 `end_datetime` 必须晚于 `start_datetime`，并继续保证 capacity 必须大于 0。

- 2026-05-11 iteration5 10:49:30 AEST：在 `events/forms.py` 中更新 `EventForm`，为 price 添加 `min="0"` 和 `step="0.01"`，为 capacity 添加 `min="1"`，让浏览器端输入也有基础限制。

- 2026-05-11 iteration5 10:49:30 AEST：在 `events/forms.py` 中新增 `clean_price()`，实现表单层 price validation；如果 price 小于 0，会显示 `Price cannot be negative. Use 0 for free events.`

- 2026-05-11 iteration5 10:49:30 AEST：在 `events/forms.py` 中更新 `EventForm.__init__()`，接收 `user` 参数，并根据当前用户限制 organisation queryset：普通 organiser 只能选择自己拥有且未 archived 的 organisation，admin/superuser 可以选择所有未 archived organisations。

- 2026-05-11 iteration5 10:49:30 AEST：在 `events/forms.py` 中为 organisation、category、venue、capacity、price、status 添加 help text，解释 organiser 自动分配、免费活动价格和后续 admin review publishing 逻辑。

- 2026-05-11 iteration5 10:49:30 AEST：在 `events/forms.py` 中新增 `has_available_organisations`、`has_available_categories` 和 `has_available_venues` 标记，用于 template 显示空下拉框 warning。

- 2026-05-11 iteration5 10:49:30 AEST：在 `events/views.py` 中更新 `event_create()`，继续在 GET 和 POST 时传入 `user=request.user`，并在当前 organiser 没有可用 organisation 时显示 warning message。

- 2026-05-11 iteration5 10:49:30 AEST：在 `events/views.py` 中更新 `event_edit()`，保存时不修改原 organiser，确保 organiser ownership 不会被表单提交改变。

- 2026-05-11 iteration5 10:49:30 AEST：在 `templates/events/event_form.html` 中新增顶部说明，提示 organiser 会根据登录用户自动分配，free event 应使用 price 0。

- 2026-05-11 iteration5 10:49:30 AEST：在 `templates/events/event_form.html` 中新增 organisation/category/venue 空数据 warning，提示需要先在 Django Admin 创建基础数据。

- 2026-05-11 iteration5 10:49:30 AEST：在 `static/css/main.css` 中新增 `warning` message 和 `help-panel` 样式，使 EventForm 的提示信息更清楚。

- 2026-05-11 iteration5 10:49:30 AEST：新增 `events/management/commands/seed_demo_data.py`，实现本地测试数据命令，使用 `get_or_create` 创建 Workshop、Networking、Music、Sports categories 和三个 demo venues。

- 2026-05-11 iteration5 10:49:30 AEST：在 `seed_demo_data` command 中新增 organiser demo organisation 和 active subscription 创建逻辑；如果存在 organiser 用户，则为第一个 organiser 创建 `Demo Student Society` 和 `Demo Plan` subscription。

- 2026-05-11 iteration5 10:49:30 AEST：运行 `.venv/bin/python manage.py check`，确认本次 Event Create/Edit 修复通过 Django 系统检查。

- 2026-05-11 iteration5 10:49:30 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本次没有新增数据库字段，不需要新的 migration。

- 2026-05-11 iteration5 10:49:30 AEST：运行 `.venv/bin/python manage.py seed_demo_data --help`，确认 Django 可以正确发现并加载新的 seed demo data command。

## 2026-05-13

- 2026-05-13 iteration1 15:06:00 AEST：在 `events/models.py` 中为 `Event` 新增可选 `image` 字段，实现 event 卡片和 event detail 页的轻量图片展示，不影响 Session 和现有权限逻辑。

- 2026-05-13 iteration1 15:06:00 AEST：在 `requirements.txt` 中新增 `Pillow`，为 Django `ImageField` 提供图片处理依赖。

- 2026-05-13 iteration1 15:06:00 AEST：在 `config/settings.py` 中新增 `MEDIA_URL` 和 `MEDIA_ROOT`，支持开发环境本地上传图片文件。

- 2026-05-13 iteration1 15:06:00 AEST：在 `config/urls.py` 中新增 DEBUG 模式下的 media file serving，确保开发时可以直接预览上传的 event 图片。

- 2026-05-13 iteration1 15:06:00 AEST：在 `events/forms.py` 中把 `image` 加入 `EventForm`，并添加可选图片 help text，继续保持 organiser 不能通过表单选择 organiser，且不改变原有 status、subscription 和 organisation 限制逻辑。

- 2026-05-13 iteration1 15:06:00 AEST：在 `events/views.py` 中更新 `event_create()` 和 `event_edit()`，加入 `request.FILES` 处理，确保 organiser 创建和编辑 event 时上传的图片可以正常保存。

- 2026-05-13 iteration1 15:06:00 AEST：在 `templates/events/event_form.html` 中为 event create/edit 表单新增 `multipart/form-data`，显示 image 字段，并在编辑已有 event 时显示当前图片预览。

- 2026-05-13 iteration1 15:06:00 AEST：在 `templates/events/event_list.html` 和 `templates/events/event_detail.html` 中新增 event image 展示与 placeholder，提升 public event list 和 event detail 的视觉效果，同时保持无图 event 正常展示。

- 2026-05-13 iteration1 15:06:00 AEST：在 `static/css/main.css` 中新增响应式 event image、event card image、placeholder 和 image preview 样式，控制固定卡片高度、`object-fit: cover` 和移动端不溢出。

- 2026-05-11 iteration6 10:58:37 AEST：在 `events/forms.py` 中新增 `SessionForm`，基于 `ModelForm` 实现 organiser 创建和编辑 session 的表单，字段包含 title、description、start_datetime、end_datetime 和 capacity。

- 2026-05-11 iteration6 10:58:37 AEST：在 `events/forms.py` 中为 `SessionForm` 设置 `datetime-local` widget 和 capacity `min="1"`，并通过 `event` 参数校验 session 时间必须位于所属 event 的时间范围内。

- 2026-05-11 iteration6 10:58:37 AEST：在 `events/forms.py` 中明确 session 的 event 不出现在表单中，session 所属 event 必须由 URL 中的 `event_id` 在 view 中自动设置。

- 2026-05-11 iteration6 10:58:37 AEST：在 `events/views.py` 中新增 `session_list()`，实现查看指定 event 下所有 sessions，并复用 `can_manage_event()` 保护 organiser ownership。

- 2026-05-11 iteration6 10:58:37 AEST：在 `events/views.py` 中新增 `session_create()`，实现 organiser 为自己 event 创建 session，保存时自动设置 `session.event`。

- 2026-05-11 iteration6 10:58:37 AEST：在 `events/views.py` 中新增 `session_edit()`，实现编辑 session；权限由 session 所属 event 决定，admin/superuser 可以编辑所有 sessions。

- 2026-05-11 iteration6 10:58:37 AEST：在 `events/views.py` 中新增 `session_delete()`，实现 session 删除确认页和 POST 删除；当前阶段 session 作为 event 子项允许真正删除。

- 2026-05-11 iteration6 10:58:37 AEST：在 `events/urls.py` 中新增 session management 路由，包括 `session_list`、`session_create`、`session_edit` 和 `session_delete`。

- 2026-05-11 iteration6 10:58:37 AEST：新增 `templates/events/session_list.html`，实现 event sessions 管理列表、Create Session 按钮、Back to Manage Events 按钮和 empty state。

- 2026-05-11 iteration6 10:58:37 AEST：新增 `templates/events/session_form.html`，实现 create/edit 共用 session 表单，包含 CSRF token、field errors、Save Session 和 Cancel 按钮。

- 2026-05-11 iteration6 10:58:37 AEST：新增 `templates/events/session_confirm_delete.html`，实现 session 删除确认页面，并提示删除后无法恢复。

- 2026-05-11 iteration6 10:58:37 AEST：在 `templates/events/organiser_event_list.html` 中新增 Manage Sessions 按钮，让 organiser 可以从 event list 进入对应 event 的 session management。

- 2026-05-11 iteration6 10:58:37 AEST：在 `templates/events/organiser_dashboard.html` 中将 Manage Sessions 从 Coming soon 更新为真实入口说明，提示先选择 event 再管理 sessions。

- 2026-05-11 iteration6 10:58:37 AEST：在 `templates/events/event_detail.html` 中新增 sessions 展示区域，如果 event 有 sessions 则显示 title、time 和 capacity，否则显示暂无 sessions。

- 2026-05-11 iteration6 10:58:37 AEST：在 `static/css/main.css` 中新增 session preview、mini list、empty state 和 session table 样式，保证 session 页面在移动端也可读。

- 2026-05-11 iteration6 10:58:37 AEST：运行 `.venv/bin/python manage.py check`，确认 Session CRUD、权限保护、templates 和 urls 配置通过 Django 系统检查。

- 2026-05-11 iteration6 10:58:37 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本阶段没有新增数据库字段，不需要新的 migration。

- 2026-05-11 iteration6 10:58:37 AEST：运行 Django test client 检查 session management 路由，未登录访问 session list/create/edit/delete 页面都会返回 302 并跳转到 login。

- 2026-05-11 iteration6 10:58:37 AEST：第六次迭代完成后，下一步建议开发 Registration + Session Selection，让 attendee 可以报名 event 并选择 sessions。

- 2026-05-11 iteration7 11:13:13 AEST：在 `events/forms.py` 中新增 `EventRegistrationForm`，使用 `ModelMultipleChoiceField` 和 `CheckboxSelectMultiple` 让 attendee 在报名 event 时选择 sessions。

- 2026-05-11 iteration7 11:13:13 AEST：在 `events/forms.py` 中让 `EventRegistrationForm` 接收 `event` 参数，并根据当前 event 动态生成 sessions queryset，避免用户选择其他 event 的 session。

- 2026-05-11 iteration7 11:13:13 AEST：在 `events/forms.py` 中新增 `get_session_remaining_capacity()` 和 `clean_sessions()`，实现至少选择一个 session、session 必须属于当前 event、session 未满员等 validation。

- 2026-05-11 iteration7 11:13:13 AEST：在 `events/views.py` 中新增 `get_event_registered_count()`、`get_session_selected_count()` 和 `add_remaining_capacity_to_sessions()`，用于计算 event/session 剩余容量并传给 template 展示。

- 2026-05-11 iteration7 11:13:13 AEST：在 `events/views.py` 中新增 `event_register()`，实现 attendee 对 published event 的报名流程，并在保存时创建 `Registration` 和对应的 `SessionSelection` 记录。

- 2026-05-11 iteration7 11:13:13 AEST：在 `events/views.py` 中为 `event_register()` 添加重复报名保护、event capacity 检查、attendee-only 权限检查，以及 archived/draft/pending event 禁止报名逻辑。

- 2026-05-11 iteration7 11:13:13 AEST：在 `events/views.py` 中新增 `my_registrations()`，实现当前用户报名记录列表，显示 event、status、selected sessions 和报名时间。

- 2026-05-11 iteration7 11:13:13 AEST：在 `events/views.py` 中新增 `registration_cancel()`，实现当前用户取消自己的 registration；取消只更新 status 为 `cancelled`，不删除历史记录。

- 2026-05-11 iteration7 11:13:13 AEST：在 `events/urls.py` 中新增 `event_register`、`my_registrations` 和 `registration_cancel` 路由。

- 2026-05-11 iteration7 11:13:13 AEST：新增 `templates/events/event_register.html`，实现 event registration 页面、sessions checkbox、剩余容量展示、Submit Registration 和 Back to Event 按钮。

- 2026-05-11 iteration7 11:13:13 AEST：新增 `templates/events/my_registrations.html`，实现用户报名记录页面，显示 selected sessions、status badge 和 Cancel Registration 按钮。

- 2026-05-11 iteration7 11:13:13 AEST：新增 `templates/events/registration_confirm_cancel.html`，实现取消报名确认页，并说明取消不会删除历史记录。

- 2026-05-11 iteration7 11:13:13 AEST：在 `templates/events/event_detail.html` 中新增 Register for Event、Already registered、View My Registrations 按钮逻辑，并在 sessions 区域显示 remaining capacity。

- 2026-05-11 iteration7 11:13:13 AEST：在 `templates/base.html` 中新增 My Registrations 导航链接，方便已登录 attendee 查看自己的报名记录。

- 2026-05-11 iteration7 11:13:13 AEST：在 `static/css/main.css` 中新增 registration form、session checkbox card、registration card、capacity text 和 registration status badge 样式。

- 2026-05-11 iteration7 11:13:13 AEST：运行 `.venv/bin/python manage.py check`，确认 Registration + Session Selection workflow 通过 Django 系统检查。

- 2026-05-11 iteration7 11:13:13 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本阶段使用既有 `Registration` 和 `SessionSelection` models，不需要新的 migration。

- 2026-05-11 iteration7 11:13:13 AEST：运行 Django test client 检查 `/events/my-registrations/`、`/events/1/register/` 和 `/events/registrations/1/cancel/`，未登录用户都会返回 302 并跳转到 login。

- 2026-05-11 iteration7 11:13:13 AEST：第七次迭代完成后，下一步建议开发 organiser registration tracking dashboard，让 organiser 可以查看自己 events 的报名人数和 session selection 情况。

- 2026-05-11 iteration8 11:31:26 AEST：在 `events/forms.py` 中增强 `SessionForm.clean()`，新增 session capacity 不能超过 event 总报名 capacity 的 validation，并提示 `Session capacity cannot exceed the total event capacity.`

- 2026-05-11 iteration8 11:31:26 AEST：在 `events/forms.py` 中更新 `EventRegistrationForm.clean_sessions()`，将 session 满员错误统一为 `One or more selected sessions are full.`，避免具体 session 与 event capacity 概念混淆。

- 2026-05-11 iteration8 11:31:26 AEST：在 `events/forms.py` 和 `events/views.py` 中将 remaining capacity 统一钳制为不小于 0，避免历史数据超过 capacity 时 UI 显示负数 remaining。

- 2026-05-11 iteration8 11:31:26 AEST：在 `events/views.py` 中优化 `event_register()` 的 event full 判断，event remaining capacity 小于等于 0 时不允许 POST 报名，并显示 `This event has reached its total registration capacity.`

- 2026-05-11 iteration8 11:31:26 AEST：在 `templates/events/event_detail.html` 中将 capacity 标签改为 `Event registration capacity`，并新增说明 `Event capacity controls the total number of registrations.`

- 2026-05-11 iteration8 11:31:26 AEST：在 `templates/events/event_detail.html` 中更新 sessions capacity 展示，明确显示 `Session capacity`，并在 session 满员时显示 `Session Full` badge。

- 2026-05-11 iteration8 11:31:26 AEST：在 `templates/events/event_detail.html` 中新增 event full 提示和 disabled Event Full 按钮，event 满员时不再显示可点击的 Register for Event 按钮。

- 2026-05-11 iteration8 11:31:26 AEST：在 `templates/events/event_register.html` 中新增 capacity 说明，明确 event capacity 控制总报名人数，session capacity 控制单个 session 的可选名额。

- 2026-05-11 iteration8 11:31:26 AEST：在 `templates/events/event_register.html` 中更新 session checkbox 渲染，session 满员时显示 Full badge 并禁用对应 checkbox。

- 2026-05-11 iteration8 11:31:26 AEST：在 `templates/events/session_form.html` 中新增说明 `Session capacity cannot exceed the event's total registration capacity.`

- 2026-05-11 iteration8 11:31:26 AEST：在 `static/css/main.css` 中新增 `.capacity-help`、`.full-badge`、`.btn-disabled` 和 disabled session checkbox 样式。

- 2026-05-11 iteration8 11:31:26 AEST：运行 `.venv/bin/python manage.py check`，确认 capacity validation 和 display 修复通过 Django 系统检查。

- 2026-05-11 iteration8 11:31:26 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本次只修改 validation/template/CSS，不需要新的 migration。

- 2026-05-11 iteration9 11:54:02 AEST：在 `events/views.py` 中新增 `add_capacity_to_events()`，为 organiser event list 临时计算 active registrations、remaining capacity 和 full 状态。

- 2026-05-11 iteration9 11:54:02 AEST：在 `events/views.py` 中增强 `organiser_dashboard()`，新增 events 数量、active registrations 数量、sessions 数量和 full sessions 数量统计；admin/superuser 显示全平台数据，普通 organiser 只显示自己的 events 数据。

- 2026-05-11 iteration9 11:54:02 AEST：在 `events/views.py` 中更新 `organiser_event_list()`，为每个 event 显示 `registered_count / capacity`、remaining capacity 和 Full badge。

- 2026-05-11 iteration9 11:54:02 AEST：在 `events/views.py` 中新增 `event_registrations()`，实现 organiser 查看单个 event 的报名列表、active capacity 和 session capacity overview。

- 2026-05-11 iteration9 11:54:02 AEST：在 `events/views.py` 中为 `event_registrations()` 复用 `can_manage_event()`，确保普通 organiser 只能查看自己创建的 event registrations，admin/superuser 可以查看全部。

- 2026-05-11 iteration9 11:54:02 AEST：在 `events/views.py` 中明确 capacity 只统计 `status='registered'` 的 active registrations，cancelled registrations 保留在列表中但不占用 event/session capacity。

- 2026-05-11 iteration9 11:54:02 AEST：在 `events/urls.py` 中新增 `event_registrations` 路由：`organiser/events/<int:event_id>/registrations/`。

- 2026-05-11 iteration9 11:54:02 AEST：在 `templates/events/organiser_dashboard.html` 中新增 dashboard stat cards，显示 Events、Active Registrations、Sessions 和 Full Sessions。

- 2026-05-11 iteration9 11:54:02 AEST：在 `templates/events/organiser_event_list.html` 中新增 View Registrations 按钮，并显示 event registration capacity 使用情况。

- 2026-05-11 iteration9 11:54:02 AEST：新增 `templates/events/event_registrations.html`，实现 Event Registrations 页面，包含 event summary、session capacity overview 和 registration list。

- 2026-05-11 iteration9 11:54:02 AEST：在 `templates/events/event_registrations.html` 中为每个 session 显示 selected count、capacity、remaining 和 Available/Full badge。

- 2026-05-11 iteration9 11:54:02 AEST：在 `templates/events/event_registrations.html` 中为每条 registration 显示 attendee username、email、status、registered at 和 selected sessions。

- 2026-05-11 iteration9 11:54:02 AEST：在 `static/css/main.css` 中新增 dashboard stat cards、summary card、section block 和 Available badge 样式，支持 organiser registration tracking 页面。

- 2026-05-11 iteration9 11:54:02 AEST：运行 `.venv/bin/python manage.py check`，确认 Organiser Registration Tracking + Session Capacity Dashboard 通过 Django 系统检查。

- 2026-05-11 iteration9 11:54:02 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本阶段只新增 views/templates/CSS，不需要新的 migration。

- 2026-05-11 iteration9 11:54:02 AEST：运行 Django test client 检查 `/events/organiser/events/1/registrations/`，未登录访问会返回 302 并跳转到 login。

- 2026-05-11 iteration9 11:54:02 AEST：第九次迭代完成后，下一步建议完善 subscriptions admin UI 或实现 recommendation algorithm。

- 2026-05-11 iteration10 11:59:59 AEST：在 `templates/events/organiser_dashboard.html` 中简化 organiser dashboard action cards，只保留 Manage Events 和 Create Event 两个主要入口。

- 2026-05-11 iteration10 11:59:59 AEST：在 `templates/events/organiser_dashboard.html` 中移除 dashboard 上单独的 Manage Sessions 和 View Registrations cards，避免与 event row 中的具体 event 操作重复。

- 2026-05-11 iteration10 11:59:59 AEST：在 `templates/events/organiser_dashboard.html` 中更新 Manage Events card 文案，说明 event editing、session management、registration tracking 和 archive 都集中在 Manage Events 页面。

- 2026-05-11 iteration10 11:59:59 AEST：在 `templates/events/organiser_event_list.html` 中新增页面说明，强调每个 event row 中提供 Edit、Manage Sessions、View Registrations 和 Archive 操作。

- 2026-05-11 iteration10 11:59:59 AEST：运行 `.venv/bin/python manage.py check`，确认 organiser dashboard workflow 简化后项目配置正常。

- 2026-05-11 iteration10 11:59:59 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本次只修改 templates，不需要新的 migration。

- 2026-05-11 iteration11 12:04:53 AEST：在 `subscriptions/forms.py` 中新增 `SubscriptionForm`，基于 `ModelForm` 实现 subscription create/edit 表单，字段包含 organisation、plan_name、status、start_date 和 end_date。

- 2026-05-11 iteration11 12:04:53 AEST：在 `subscriptions/forms.py` 中为 start_date 和 end_date 设置 date input，并新增 validation：end_date 不能早于 start_date。

- 2026-05-11 iteration11 12:04:53 AEST：在 `subscriptions/views.py` 中更新 `subscription_list()`，实现 admin-only subscription 管理列表，支持每页 10 条分页、status filter 和 keyword search。

- 2026-05-11 iteration11 12:04:53 AEST：在 `subscriptions/views.py` 中新增 `subscription_create()`，实现自定义页面创建 SaaS subscription。

- 2026-05-11 iteration11 12:04:53 AEST：在 `subscriptions/views.py` 中新增 `subscription_edit()`，实现自定义页面编辑 SaaS subscription。

- 2026-05-11 iteration11 12:04:53 AEST：在 `subscriptions/views.py` 中新增 `subscription_archive()`，实现 archive subscription；archive 只将 status 改为 `archived`，不删除数据库记录。

- 2026-05-11 iteration11 12:04:53 AEST：在 `subscriptions/urls.py` 中新增 `subscription_create`、`subscription_edit` 和 `subscription_archive` 路由。

- 2026-05-11 iteration11 12:04:53 AEST：在 `templates/subscriptions/subscription_list.html` 中实现 Subscription Management 页面，包含 Create Subscription、搜索过滤表单、subscription table、Archived badge 和分页控件。

- 2026-05-11 iteration11 12:04:53 AEST：新增 `templates/subscriptions/subscription_form.html`，实现 create/edit 共用 subscription 表单，包含 CSRF token、form errors、Save 和 Cancel。

- 2026-05-11 iteration11 12:04:53 AEST：新增 `templates/subscriptions/subscription_confirm_archive.html`，实现 archive 确认页面，并说明 archive 会保留记录但标记为 inactive。

- 2026-05-11 iteration11 12:04:53 AEST：在 `static/css/main.css` 中新增 subscription status expired 样式和 pagination 样式，复用现有 table、badge 和 button 设计。

- 2026-05-11 iteration11 12:04:53 AEST：运行 `.venv/bin/python manage.py check`，确认 Admin Subscription Management 自定义页面通过 Django 系统检查。

- 2026-05-11 iteration11 12:04:53 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本阶段只新增 forms/views/templates/CSS，不需要新的 migration。

- 2026-05-11 iteration11 12:04:53 AEST：运行 Django test client 检查 `/subscriptions/`、`/subscriptions/create/`、`/subscriptions/1/edit/` 和 `/subscriptions/1/archive/`，未登录访问都会返回 302 并跳转到 login。

- 2026-05-11 iteration11 12:04:53 AEST：第十一次迭代完成后，下一步建议实现 recommendation algorithm 或 deployment preparation。

- 2026-05-11 iteration12 12:20:21 AEST：在 `accounts/forms.py` 中更新 `RegisterForm`，移除 role 字段，新注册用户默认创建为 attendee，organiser access 必须由平台管理员手动批准。

- 2026-05-11 iteration12 12:20:21 AEST：在 `templates/accounts/register.html` 中移除 role 选择 UI，并新增说明 `Organiser access must be approved by a platform administrator.`

- 2026-05-11 iteration12 12:20:21 AEST：在 `subscriptions/models.py` 中新增 `Organisation.has_active_subscription()`，用于判断 organisation 是否拥有当前有效 active subscription。

- 2026-05-11 iteration12 12:20:21 AEST：在 `subscriptions/models.py` 中新增 `Subscription.is_currently_active()`，用于判断 subscription status 和日期范围是否当前有效。

- 2026-05-11 iteration12 12:20:21 AEST：在 `events/forms.py` 中更新 `EventForm.__init__()`，普通 organiser 创建 event 时只能选择自己拥有、status active、且拥有当前有效 subscription 的 organisation。

- 2026-05-11 iteration12 12:20:21 AEST：在 `events/forms.py` 中限制普通 organiser 的 event status choices 为 draft 和 pending；admin/superuser 仍可设置 draft、pending、published、archived。

- 2026-05-11 iteration12 12:20:21 AEST：在 `events/forms.py` 中新增 `has_publishing_access` 标记，用于 create event 页面判断当前 organiser 是否拥有创建新 event 的 subscription 权限。

- 2026-05-11 iteration12 12:20:21 AEST：在 `events/views.py` 中更新 `organiser_dashboard()`，当 organiser 没有 active subscription organisation 时显示 publishing access warning，但仍允许查看历史 records。

- 2026-05-11 iteration12 12:20:21 AEST：在 `events/views.py` 中更新 `event_create()`，如果普通 organiser 没有 active subscription organisation，则阻止创建新 event 并提示联系 platform administrator。

- 2026-05-11 iteration12 12:20:21 AEST：在 `templates/events/event_form.html` 中新增 admin approval 文案，说明 organiser 创建的 events 需要 admin approval 后才会公开显示。

- 2026-05-11 iteration12 12:20:21 AEST：在 `templates/events/event_form.html` 中新增 publishing access warning，并在无 active subscription 时隐藏 Save Event，显示 disabled Publishing Access Required 按钮。

- 2026-05-11 iteration12 12:20:21 AEST：在 `templates/events/event_detail.html` 中为 archived event owner/admin/superuser 显示 warning，说明 archived event 对 public users 隐藏但保留给 organiser/admin records。

- 2026-05-11 iteration12 12:20:21 AEST：在 `templates/subscriptions/subscription_list.html` 中新增 expired subscription visual warning；当 subscription status 仍为 active 但日期已过期时显示 `Active status, but date expired`。

- 2026-05-11 iteration12 12:20:21 AEST：本次修补明确 subscription 控制 organisation 的平台使用资格，event status 控制内容审核流程，两者属于不同层级的业务规则。

- 2026-05-11 iteration12 12:20:21 AEST：运行 `.venv/bin/python manage.py check`，确认 organiser approval、active subscription check、event admin approval 和 archived visibility 修补通过 Django 系统检查。

- 2026-05-11 iteration12 12:20:21 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本次只新增 helper/methods 和业务逻辑，不需要新的 migration。

- 2026-05-11 iteration13 13:12:52 AEST：在 `events/views.py` 中新增 `can_write_event()`，实现 subscription inactive 后普通 organiser 进入 read-only mode；admin/superuser 不受限制。

- 2026-05-11 iteration13 13:12:52 AEST：在 `events/views.py` 中新增 `add_write_access_to_events()`，为 organiser event list 中的每个 event 临时添加 `can_write` 和 `is_readonly` 状态。

- 2026-05-11 iteration13 13:12:52 AEST：在 `events/views.py` 中更新 `event_edit()`，当普通 organiser 的 event organisation 没有 active subscription 或 event 已 archived 时，阻止编辑并提示 existing events are read-only。

- 2026-05-11 iteration13 13:12:52 AEST：在 `events/views.py` 中更新 `event_archive()`，将 archive 视为写操作；subscription inactive 后普通 organiser 不能 archive event。

- 2026-05-11 iteration13 13:12:52 AEST：在 `events/views.py` 中更新 `session_create()`、`session_edit()` 和 `session_delete()`，subscription inactive 后普通 organiser 不能 create/edit/delete sessions，只能查看历史 sessions。

- 2026-05-11 iteration13 13:12:52 AEST：在 `events/views.py` 中更新 `session_list()` 和 `event_detail()` context，向模板传入 `can_write` 用于隐藏写操作按钮。

- 2026-05-11 iteration13 13:12:52 AEST：在 `templates/events/organiser_event_list.html` 中根据 `event.can_write` 控制按钮显示；read-only event 只显示 View、View Registrations、View Sessions，并显示 `Read-only: subscription inactive` badge。

- 2026-05-11 iteration13 13:12:52 AEST：在 `templates/events/session_list.html` 中为 inactive subscription 显示 read-only warning，并隐藏 Create/Edit/Delete session 按钮。

- 2026-05-11 iteration13 13:12:52 AEST：在 `templates/events/event_detail.html` 中为 read-only event 显示 warning，只保留 Back to Manage Events 和 View Registrations，不显示 Manage Sessions 写入口。

- 2026-05-11 iteration13 13:12:52 AEST：在 `templates/events/organiser_event_list.html` 中当 organiser 没有 active subscription organisation 时禁用 Create New Event 按钮，并显示只能查看历史 records 的 warning。

- 2026-05-11 iteration13 13:12:52 AEST：在 `static/css/main.css` 中新增 `.badge-readonly` 和 `.warning-box` 样式，保持现有 UI 风格下突出 read-only 状态。

- 2026-05-11 iteration13 13:12:52 AEST：本次权限修复确认 archived event 继续对 public users 隐藏，但 event owner organiser、admin、superuser 仍可查看；普通 organiser 不能编辑 archived event 或管理其 sessions。

- 2026-05-11 iteration13 13:12:52 AEST：运行 `.venv/bin/python manage.py check`，确认 inactive subscription read-only mode 通过 Django 系统检查。

- 2026-05-11 iteration13 13:12:52 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本次只修改权限逻辑和模板，不需要新的 migration。

- 2026-05-11 iteration14 13:20:33 AEST：新增 `events/recommendations.py`，实现不使用外部 AI API 的 rule-based Event Recommendation Algorithm。

- 2026-05-11 iteration14 13:20:33 AEST：在 `events/recommendations.py` 中新增 capacity helper：`get_event_registered_count()`、`get_event_remaining_capacity()` 和 `session_has_remaining_capacity()`，并且只统计 `Registration.status='registered'`。

- 2026-05-11 iteration14 13:20:33 AEST：在 `events/recommendations.py` 中新增 `get_recommended_events(user, limit=10)`，只推荐 published events，并排除 already registered、full events、没有可用 session 的 events，以及 draft/pending/archived events。

- 2026-05-11 iteration14 13:20:33 AEST：在 recommendation scoring 中新增可解释规则：category match +5、organisation match +3、event remaining capacity +2、session remaining capacity +2、未来 14 天内开始 +1。

- 2026-05-11 iteration14 13:20:33 AEST：在 recommendation algorithm 中为没有历史 registration 的用户提供 fallback，推荐 upcoming published events with available capacity，并显示 `Available upcoming event` reason。

- 2026-05-11 iteration14 13:20:33 AEST：在 `events/views.py` 中新增 `recommended_events()` view，要求 login，并调用 `get_recommended_events(request.user)` 渲染推荐页面。

- 2026-05-11 iteration14 13:20:33 AEST：在 `events/urls.py` 中新增 `recommended/` 路由，URL name 为 `recommended_events`。

- 2026-05-11 iteration14 13:20:33 AEST：新增 `templates/events/recommended_events.html`，显示推荐 event cards、score、reasons、remaining capacity 和 View Details 按钮。

- 2026-05-11 iteration14 13:20:33 AEST：在 `templates/base.html` 中为已登录用户新增 Recommended 导航链接。

- 2026-05-11 iteration14 13:20:33 AEST：在 `templates/events/event_list.html` 中为已登录用户新增 `View Recommended Events` 入口。

- 2026-05-11 iteration14 13:20:33 AEST：在 `static/css/main.css` 中新增 recommendation card、recommendation score、reason badge 和 inline link 样式。

- 2026-05-11 iteration14 13:20:33 AEST：运行 `.venv/bin/python manage.py check`，确认 recommendation algorithm 页面和路由通过 Django 系统检查。

- 2026-05-11 iteration14 13:20:33 AEST：运行 `.venv/bin/python manage.py makemigrations --dry-run --check`，确认本阶段只新增 algorithm/view/template/CSS，不需要新的 migration。

- 2026-05-11 iteration14 13:20:33 AEST：运行 Django test client 检查 `/events/recommended/`，未登录访问会返回 302 并跳转到 login。

- 2026-05-13 iteration15 14:07:27 AEST：在 `events/management/commands/seed_demo_data.py` 中增强 demo data，新增用于 recommendation testing 的 demo events 和 sessions。

- 2026-05-13 iteration15 14:07:27 AEST：在 `seed_demo_data` command 中新增 4 个 published events：`Music Workshop`、`Music Networking Night`、`Sports Meetup` 和 `Tech Career Talk`，用于推荐算法 demo。

- 2026-05-13 iteration15 14:07:27 AEST：在 `seed_demo_data` command 中新增 `Pending Admin Review Event`，status 为 pending，用于验证 recommendation algorithm 不推荐非 published events。

- 2026-05-13 iteration15 14:07:27 AEST：在 `seed_demo_data` command 中为每个 demo event 创建至少一个 session，并使用 `get_or_create` 避免重复创建同名 event/session。

- 2026-05-13 iteration15 14:07:27 AEST：在 `templates/events/recommended_events.html` 中优化 empty state，新增没有推荐结果的可能原因：用户可能已注册所有可用 events、部分 events 可能已满、只有 published 且有可用 sessions 的 events 会被推荐。

- 2026-05-13 iteration15 14:07:27 AEST：运行 `.venv/bin/python manage.py check`，确认增强 seed demo data 和 recommendation empty state 后项目通过 Django 系统检查。

- 2026-05-13 iteration15 14:07:27 AEST：运行 `.venv/bin/python manage.py seed_demo_data --help`，确认增强后的 seed command 可以被 Django 正确加载。

- 2026-05-13 iteration16 14:28:57 AEST：新增 `TESTING_CHECKLIST.md`，按 visitor、attendee、active subscription organiser、inactive subscription organiser、admin/superuser、UI/responsive/accessibility、deployment 七类组织正式验收测试清单。

- 2026-05-13 iteration16 14:28:57 AEST：新增 `CODE_REVIEW_NOTES.md`，整理 authentication、role authorization、subscription management、Event CRUD、Session CRUD、Registration、capacity tracking、recommendation algorithm 和 UI templates 的代码位置与讲解要点。

- 2026-05-13 iteration16 14:28:57 AEST：更新 `README.md`，补充 Project Overview、Tech Stack、Local Setup、How to Run、Demo Accounts、Deployment URL placeholder、rubric feature mapping、recommendation algorithm explanation、security summary 和 GenAI Usage Declaration。

- 2026-05-13 iteration16 14:28:57 AEST：在 `README.md` 中新增 Testing 和 Code Review Preparation 链接，指向 `TESTING_CHECKLIST.md` 和 `CODE_REVIEW_NOTES.md`，方便 Project Demonstration & Code Review 准备。

- 2026-05-13 iteration17 15:18:00 AEST：在 `DEVELOPMENT_LOG.md` 中补充并整理 event image 功能相关开发记录，确保 `Event.image`、`Pillow`、`MEDIA_URL/MEDIA_ROOT`、event form multipart upload、event list/detail 图片展示与 responsive image styles 的本次迭代有完整可追溯日志。

- 2026-05-13 iteration18 15:34:00 AEST：在 `templates/events/event_detail.html`、`templates/events/event_list.html`、`templates/events/recommended_events.html` 和 `static/css/main.css` 中修复 oversized event image display，调整 detail banner、card thumbnail 和 placeholder 尺寸，避免原图按原始大小撑开页面。

- 2026-05-13 iteration18 15:34:00 AEST：在 `static/css/main.css` 中新增和修正 responsive image styles，包括 `.event-detail-image`、`.event-card-image`、`.event-image-preview` 和 `.event-image-placeholder`，确保 450px 手机宽度下图片高度收敛且不横向溢出。

- 2026-05-13 iteration18 15:34:00 AEST：在 `templates/events/event_detail.html`、`templates/events/event_list.html`、`templates/events/recommended_events.html` 和 `templates/events/event_form.html` 中补充安全 alt text 和 placeholder display，并继续先判断图片字段存在后才访问 `.url`。

- 2026-05-13 iteration18 15:34:00 AEST：在 `events/forms.py` 中新增基础 image size/type validation，仅允许 `jpg`、`jpeg`、`png`、`webp` 且限制 3MB 以内，不引入自动压缩或复杂图片处理逻辑。

- 2026-05-13 iteration19 15:49:00 AEST：在 `templates/events/event_list.html` 和 `templates/events/recommended_events.html` 中修复 event image overflow issue，把 event images 移入 `event-card-image-wrap` 和 `event-card-body` 结构内部，避免图片穿透到其他 cards 后面。

- 2026-05-13 iteration19 15:49:00 AEST：在 `static/css/main.css` 中新增固定高度 image wrappers 和 `object-fit: cover` 样式，确保 event list/recommended/detail 的图片显示被限制在各自组件边界内，不再作为背景或超出 card 范围。

- 2026-05-13 iteration19 15:49:00 AEST：在 `templates/events/event_detail.html` 和 `static/css/main.css` 中更新 detail banner image 和 placeholder 结构，确保 event detail 图片响应式显示且不会撑破页面布局。

- 2026-05-13 iteration20 16:00:00 AEST：在 `templates/events/event_list.html` 和 `templates/events/recommended_events.html` 中确认并固定 event_list image DOM structure，确保所有 event image 仅出现在 `event-card-image-wrap` 内部，正文内容统一放入 `event-card-body`。

- 2026-05-13 iteration20 16:00:00 AEST：在 `static/css/main.css` 末尾追加更靠后的覆盖规则，确保 event image 被限制在 fixed-height wrapper 内，使用 `object-fit: cover` 显示，不再按原始比例把 event card 撑高。

- 2026-05-13 iteration20 16:00:00 AEST：在 `static/css/main.css` 中移除或覆盖 event image 相关冲突效果，通过更具体的 `.event-card-image-wrap > .event-card-image` 和 placeholder 规则消除旧样式干扰。

- 2026-05-13 iteration21 16:08:00 AEST：在 `static/css/main.css` 中进一步固定 event image 显示尺寸，把 card 图片改为绝对定位填充 `event-card-image-wrap`，并移除 `max-width: none` 的冲突影响，确保任何尺寸的图片都只能显示为固定高度缩略图。

- 2026-05-13 iteration22 16:34:00 AEST：参考之前的 HTML mockup/doc1 作为视觉风格来源，在 `templates/base.html`、`templates/home.html`、`templates/events/*`、`templates/accounts/*`、`templates/subscriptions/*` 和 `static/css/main.css` 中统一升级页面视觉，延续 blue/purple gradient、clean white cards、rounded corners 和 clearer workflow 设计。

- 2026-05-13 iteration22 16:34:00 AEST：在 public-facing 页面中重点增强 event browsing experience，优化 `/`、`/events/`、`/events/recommended/`、event detail 和 registration 页面，使其更像完整 event website，同时保留现有 Django dynamic workflows、permissions、image checks、CSRF 和 role-based navigation。

- 2026-05-13 iteration22 16:34:00 AEST：在 management 页面中统一 cards、buttons、forms、badges、table wrapper 和 warnings，明确 create/edit/archive/session management/registration tracking/subscription management 入口，提升 organiser/admin workflow clarity。

- 2026-05-13 iteration22 16:34:00 AEST：在 `static/css/main.css` 中完善 450px 附近的 responsive layout，包括 nav wrapping、single-column cards、table horizontal scroll、readable forms 和 fixed event image containers，避免 mobile 下布局拥挤和图片溢出。

- 2026-05-13 iteration22 16:34:00 AEST：在模板和样式中加强 accessibility，包括 skip link、visible labels、message live region、focus-visible states、status text badges、clear danger action labels 和 non-colour-only state communication。

- 2026-05-13 iteration23 16:49:00 AEST：读取 `mock-ups/` 文件夹中的 `index.html`、`events.html`、`event-detail.html`、`event-form.html`、`register.html`、`organiser-dashboard.html` 和 `admin-dashboard.html` 作为视觉参考，继续对当前 Django 前端做 mockup-aligned 优化，同时保留现有动态模板逻辑和权限分支。

- 2026-05-13 iteration23 16:49:00 AEST：在 `templates/home.html` 和 `static/css/main.css` 中进一步向原始 landing mockup 靠拢，新增 search card、popular categories cards 和 browse events callout，使首页更接近早期 UI/UX mockup 的结构与层次。

- 2026-05-13 iteration23 16:49:00 AEST：在 `static/css/main.css` 中修正 skip link 的可见性行为，改为默认视觉隐藏、仅在键盘 focus 时显示，避免页面左上角长期出现可见跳转按钮。

- 2026-05-13 iteration24 17:03:00 AEST：在 `static/css/main.css` 中修复 Home 页 Popular Categories cards 的低对比度问题，把 category cards 调整为白底、深色文字、金色顶部强调线和浅紫边框，避免浅色半透明背景上使用白色文字。

- 2026-05-13 iteration24 17:03:00 AEST：在 `static/css/main.css` 中增强 UQ-inspired theme accessibility，统一检查并调整 card text/background colours、danger button contrast 和 gold focus-visible outline，提升整体可读性而不改变现有 workflow。

- 2026-05-13 iteration25 17:14:00 AEST：在 `templates/home.html` 中改进 Popular Categories interaction，把分类卡片从统一跳转 `/events/` 改为链接到带查询参数的 filtered event browsing，提升从 Home 到 Events 的 workflow clarity，同时保留 mock-up inspired visual design。

- 2026-05-13 iteration25 17:14:00 AEST：在 `static/css/main.css` 中为 category cards 新增更明确的交互提示文案和 hover/focus 状态，强化可点击性提示而不改变现有 Django event list filter 逻辑。

- 2026-05-13 iteration26 17:34:00 AEST：修复 organiser ownership authorization，在 `events/views.py` 中把普通 organiser 的 event ownership 判断从 `event.organiser == user` 调整为 organisation ownership 级别，确保 SaaS subscription / organisation 数据隔离逻辑成立。

- 2026-05-13 iteration26 17:34:00 AEST：在 organiser dashboard 和 manage events queryset 中限制普通 organiser 只能看到自己 organisation 下的 events，同时保留 admin/superuser 的全局管理访问能力。

- 2026-05-13 iteration26 17:34:00 AEST：在 `event_edit`、`event_archive`、`session_list`、`session_create`、`session_edit`、`session_delete` 和 `event_registrations` 中补强 URL-based access protection，阻止普通 organiser 通过直接访问 URL 管理其他 organisation 的 event/session/registration 数据。

- 2026-05-13 iteration26 17:34:00 AEST：在 `event_create` 中增加 defence-in-depth 检查，确保普通 organiser 只能为自己 organisation 且具备 active subscription 的 organisation 创建 event，并保持 inactive subscription read-only behaviour 与 admin/superuser 全局管理能力不变。

- 2026-05-13 iteration27 18:02:00 AEST：新增 organiser access / organisation request workflow，在 `subscriptions` app 中加入登录用户可提交的 organisation request 表单与页面，使用现有 `Organisation` model 创建 pending organisation 记录，避免引入复杂新模型。

- 2026-05-13 iteration27 18:02:00 AEST：澄清 subscription 是 organiser publishing permission，而不是 attendee permission；在 `event_register` 与 event detail register button 中允许 organiser 继续报名 published public events，同时保留 admin/superuser 不参与 attendee registration workflow。

- 2026-05-13 iteration27 18:02:00 AEST：在 Subscription Management 中加入 pending organisation admin handling，显示 pending organisations section，并支持通过创建 subscription 激活 organisation、提升 owner 为 organiser，以及拒绝 pending request。

- 2026-05-13 iteration27 18:02:00 AEST：新增 subscription reactivation flow，admin 可通过 POST 重新激活 archived/expired subscription，并同步恢复 organisation active 状态与 owner organiser publishing access。

- 2026-05-13 iteration27 18:02:00 AEST：保持之前的 organiser ownership authorization，不改变 event/session/registration/recommendation 既有核心业务逻辑，只补强申请、审批、激活与 read-only 提示链路。

- 2026-05-14 iteration28 09:18:00 AEST：统一全站按钮组件，在 `static/css/main.css` 中整理并补充 `.btn`、`.btn-primary`、`.btn-secondary`、`.btn-danger`、`.btn-success`、`.btn-disabled`、`.btn-small`、`.btn-group` 和 `.action-row`，同时保持旧的 `button` / `primary-button` 等 class 兼容。

- 2026-05-14 iteration28 09:18:00 AEST：优化 primary/secondary/danger/disabled action hierarchy，统一按钮高度、圆角、padding、hover/focus-visible 状态，并加强 link-style buttons 与 button elements 的视觉一致性。

- 2026-05-14 iteration28 09:18:00 AEST：在 `templates/events/event_detail.html` 中修复 Register for Event 与 Back to Events 的按钮间距，把关键操作放入更清晰的 action rows，避免按钮紧贴。

- 2026-05-14 iteration28 09:18:00 AEST：在 `templates/events/my_registrations.html`、`templates/events/organiser_event_list.html`、`templates/events/session_list.html`、`templates/subscriptions/subscription_list.html`、`templates/accounts/login.html` 和 `templates/accounts/register.html` 中统一按钮语义与表格小按钮样式，提升 management tables 与表单页面的一致性。

- 2026-05-14 iteration28 09:18:00 AEST：改进 450px 附近的 mobile button layout，默认 action rows / button groups 改为纵向堆叠，但在 `table-wrapper` 中保留横向小按钮布局，兼顾可点击性与表格紧凑度。

- 2026-05-14 iteration29 09:34:00 AEST：优化 mobile header spacing，在 `static/css/main.css` 的 450px 断点下减小 header padding、logo 字号、nav gap、nav link padding 和 username pill 尺寸，缓解移动端导航换行后占用过多高度的问题。

- 2026-05-14 iteration29 09:34:00 AEST：将 management tables 在小屏幕下转换为 responsive card layout，保留 desktop table layout，同时在 `templates/events/organiser_event_list.html`、`templates/events/session_list.html`、`templates/events/event_registrations.html` 和 `templates/subscriptions/subscription_list.html` 中新增 `responsive-table` 与 `data-label` 字段。

- 2026-05-14 iteration29 09:34:00 AEST：提升 mobile table readability 和 action button accessibility，在小屏 card rows 中把 Actions 区域移到每张卡片底部并纵向展开按钮，避免用户大量横向拖动后才能找到 Edit / Archive / Manage Sessions。

- 2026-05-14 iteration29 09:34:00 AEST：保持 desktop tables、现有 workflows、permissions、registration/capacity/subscription/recommendation 逻辑不变，只对 responsive UI 呈现做增强。

- 2026-05-14 iteration30 09:42:00 AEST：继续微调 450px 以下的 mobile header compact spacing，仅在 `static/css/main.css` 中进一步收紧 header padding、header gap、logo 字号、nav gap、nav link padding 和 `nav-user` 尺寸，减少导航换行后的垂直占用，同时保留全部导航链接与 desktop header 样式不变。

- 2026-05-14 iteration31 10:02:00 AEST：整理 UQ Cloud Zone deployment settings，在 `config/settings.py` 中改为基于环境变量读取 `SECRET_KEY`、`DEBUG`、`ALLOWED_HOSTS` 和 `CSRF_TRUSTED_ORIGINS`，同时保留本地开发 fallback 与 SQLite 默认数据库。

- 2026-05-14 iteration31 10:02:00 AEST：检查并确认 production static/media 路径，统一 `STATIC_URL=/static/`、`STATIC_ROOT=BASE_DIR / "staticfiles"`、`STATICFILES_DIRS=[BASE_DIR / "static"]`、`MEDIA_URL=/media/` 和 `MEDIA_ROOT=BASE_DIR / "media"`，以适配 UQ Cloud Zone + uwsgi312 部署流程。

- 2026-05-14 iteration31 10:02:00 AEST：更新 `requirements.txt`、`.env.example` 和 `.gitignore`，保留部署所需最小依赖与安全环境变量模板，并继续忽略本地虚拟环境、数据库、media 与 collected static 文件。

- 2026-05-14 iteration31 10:02:00 AEST：在 `README.md` 和 `TESTING_CHECKLIST.md` 中补充 UQ Cloud Zone 部署说明、sample `uwsgi.ini`、nginx static/media aliases、service restart 步骤和部署验证检查项。
