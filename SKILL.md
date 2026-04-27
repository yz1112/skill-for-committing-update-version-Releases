---
name: git-workflow
description: إدارة Git للمشروع: commit صحيح مع رفع الإصدار تلقائياً، التنقل بين فروع dev وmain، والدمج للإنتاج. استخدم هذه المهارة عند أي عملية commit أو push أو merge أو سؤال عن الفروع أو الإصدارات.
disable-model-invocation: false
---

# Git Workflow — لعبة الأسهم

## قواعد الفروع

| الفرع | الغرض | القاعدة |
|-------|--------|---------|
| `main` | الإنتاج الحي | ❌ لا تكتب كوداً مباشرةً فيه |
| `dev`  | العمل اليومي | ✅ كل تطوير يبدأ من هنا |

---

## خطوات الـ Commit الصحيح

**قبل أي `commit` أو `push` يجب رفع الإصدار أولاً:**

```bash
# 1. ارفع الإصدار حسب نوع التغيير
python bump_version.py patch    # إصلاح خطأ بسيط
python bump_version.py minor    # ميزة جديدة
python bump_version.py major    # تغيير جذري

# 2. أضف الملفات مع VERSION.txt في نفس الـ commit
git add .
git commit -m "نوع(الميزة): وصف التغيير (v1.2.0)"

# 3. ادفع إلى dev
git push origin dev
```

> ⚠️ لا تعمل commit منفصل لـ VERSION.txt — يجب أن يكون في نفس الـ commit.

---

## متى ترفع أي رقم؟

- **PATCH** `1.0.0 → 1.0.1`: إصلاح خطأ، تعديل نص، refactor
- **MINOR** `1.0.0 → 1.1.0`: ميزة جديدة، شاشة جديدة، endpoint جديد
- **MAJOR** `1.0.0 → 2.0.0`: تغيير جذري يكسر ما قبله

---

## الدمج من dev إلى main (الإنتاج)

```bash
git checkout main
git merge dev
git push origin main
```

> بعد هذا يتم النشر للمستخدمين فوراً — تأكد من الاختبار محلياً أولاً.

---

## سياسة المشروع

- **auto-commit**: بعد إتمام أي مهمة أو تعديل على الكود، قم تلقائياً برفع الإصدار المناسب وعمل commit بدون انتظار طلب صريح.
- `GET /api/version` يقرأ من `VERSION.txt` ويظهر في الـ UI — كل push يجب أن يحمل إصداراً أحدث.
