<!-- academy:title -->
# الذكاء الاصطناعي للباحثين والعمل العلمي

AI for Researchers and Scientific Work

مسار الطلاقة في البيانات والذكاء الاصطناعي · أكاديمية سدايا · USE-PRO-208 · المستوى 200

تستعين بالذكاء الاصطناعي في البحث والفرز والتلخيص والتحليل، وتبقى كل إحالة متحقَّقًا منها، وكل رقم له مصدر، وكل استخدام مُفصَحًا عنه

يستخدم الباحثون من مختلف التخصصات الذكاء الاصطناعي في مشروع اصطناعي واحد يتناول سؤالًا استكشافيًا عن التعرض للحرارة لدى العاملين في الأماكن المكشوفة، مع 200 سجل مسترجع ومجموعة بيانات عامة، بدءًا بفرز الدراسات والتحقق من الملخصات وانتهاءً بتحليل قابل لإعادة الإنتاج وبيان إفصاح. أما الممارسة البحثية لعلماء الذكاء الاصطناعي فيغطيها المقرر SPC-RSP-301.

**الصيغة:** ورشة عمل: يومان من المختبرات على حالة اصطناعية واحدة، إضافةً إلى خط أساس متعقَّب

**صفحة المقرر:** https://sdaiaacademy.github.io/use-pro-208/
<!-- /academy:title -->

## نواتج التعلم

| | نواتج التعلم | المستوى | الدليل |
|---|---|---|---|
| LO1 | يميّز بين استخدامات الذكاء الاصطناعي في البحث المقبولة والواجب الإفصاح عنها والمحظورة، استنادًا إلى اثني عشر استخدامًا، من التحرير اللغوي إلى مراجعة مخطوطة سرية | Awareness | جدول يطابق المرجع في عشرة منها |
| LO2 | يستخدم قواعد البيانات العلمية ومساعد فرز بالذكاء الاصطناعي لرسم خريطة للأدبيات ببحث موثق، استنادًا إلى سؤال استكشافي و200 سجل | Applied | سجل بحث، وقياس استدعاء المساعد مقارنة بفرز المشارك لخمسين سجلًا |
| LO3 | يختبر ملخصات أوراق علمية كتبها الذكاء الاصطناعي بحثًا عن أخطاء في نقل الفئات المدروسة والأساليب وأحجام الأثر والاستنتاجات، على عشرة ملخصات فيها أخطاء مزروعة | Applied | تدقيق يذكر لكل خطأ المقطع الذي يناقضه |
| LO4 | ينفذ تحليلًا بمساعدة الذكاء الاصطناعي وفق خطة معلنة مسبقًا، ويعيد إنتاجه من تشغيل نظيف، على مجموعة بيانات عامة | Applied | دفتر يُعاد تشغيله دون أخطاء، مع سجل قرارات |
| LO5 | يعيد تصميم مهمة بحثية واحدة باستخدام الذكاء الاصطناعي، ويقيسها في تشغيلين، ويفصح عن استخدام الذكاء الاصطناعي، استنادًا إلى خط الأساس المعدّ في العمل التحضيري | Performance | بطاقة إعادة تصميم وبيان إفصاح يستوفي سياسة مجلة محددة، يُراجَعان مباشرة |

<!-- academy:units -->
## الوحدات

| الوحدة | العنوان | الجلسات | الشرائح |
|---|---|---|---|
| اليوم 1 | النزاهة وخريطة الأدبيات | ما يُقبل وما يُفصح عنه وما يُحظر; خريطة الأدبيات: بحث موثّق وفرز يُقاس | [`slides/day1.html`](slides/day1.html) |
| اليوم 2 | الملخصات والتحليل | اقرأ المصدر لا الملخص; خطة قبل الأمر، وتشغيل نظيف | [`slides/day2.html`](slides/day2.html) |
| المشروع الختامي | جلسة المراجعة: البطاقة والإفصاح والدفتر |  | [`slides/review.html`](slides/review.html) |
<!-- /academy:units -->

## دراسة الحالة

**معهد هَجير لبحوث الصحة المهنية.** معهد بحثي افتراضي يعدّ مراجعة استكشافية عن التعرض للحرارة لدى العاملين في الأماكن المكشوفة. المشارك في دور الباحثة المشاركة بندري الميمني، ومساعد المعهد اسمه «مُعين». المعهد وأشخاصه ومجلته وسجلاته وأوراقه وأعداد زيارات عياداته كلها من صنع المقرر، ومولّدة ببذرة ثابتة.

البيانات الحقيقية الوحيدة سلسلة يومية عامة لدرجات الحرارة من مشروع NASA POWER (نقطة واحدة، من مايو إلى سبتمبر 2024)، محفوظة كما نُزّلت مع عنوان طلبها وتاريخه في `labs/files/analysis/DATA_SOURCES.txt`. أعداد الزيارات المربوطة بها اصطناعية، فكل نتيجة تخرج منها تمرين لا معلومة.

مخرجات المساعد «مُعين» في المختبرات (قرارات الفرز، والملخصات العشرة، والدفتر كما تركه) كتبها مؤلف المقرر وزرع أخطاءها. لم يكتبها نموذج.

## كيف تسير الورشة

- **قبل الورشة (نحو ساعتين):** يختار المشارك مهمة بحثية متكررة من عمله موادها منشورة أو عامة، ويؤديها مرة دون مساعد، ويسجّل دقائقها وأخطاءها في `labs/files/baseline_sheet.csv`. الدليل في `labs/files/prework_guide.txt`.
- **يومان:** في كل يوم جلستان، وفي كل جلسة قسمان من المفاهيم ينتهي كل منهما بسؤال تحقق، ثم مختبر. المختبرات الأربعة مجموعها ثلاث ساعات ونصف.
- **سياسة الذكاء الاصطناعي:** دون أي مساعد في المختبر 1.1 وفي الفحص الفردي. المساعد معلّم يسأل عن خطة التحليل ولا يكتبها. مسموح كاملًا في ما عدا ذلك، وكل استخدام يُسجَّل في `labs/files/ai_use_log.csv` ليُكتب منه بيان الإفصاح.
- **ما لا يدخل القاعة ولا أي أداة:** مخطوطة غير منشورة، أو بيانات مشاركين، أو بيانات مقيّدة.

## التقييم والمشروع الختامي

| المكوّن | الوزن |
|---|---|
| فحص فردي دون ذكاء اصطناعي: إيجاد الأخطاء في ملخصين كتبهما مساعد | 20% |
| مخرجات المختبرات الأربعة | 35% |
| بطاقة إعادة التصميم وبيان الإفصاح | 35% |
| المراجعة المباشرة | 10% |

النجاح: 70% في المجموع، ولا مرجع لم يُتحقق منه، ولا رقم لا يُعرف مصدره. مواد الفحص الفردي ليست في هذا المستودع.

**المشروع الختامي** فردي: يعيد المشارك تصميم المهمة التي قاس خط أساسها، وينفذها مرتين بمساعدة الذكاء الاصطناعي، ويكتب بيان إفصاح يستوفي سياسة مجلة يسمّيها. المثال الذي يتخذه المقرر سياسة مجلة PLOS ONE: أسماء الأدوات، وكيف استُخدمت وفي أي جزء، وكيف قُيّمت صحة مخرجاتها. يُسلَّم العمل رابطًا لمجلد مشترك، ثم مراجعة مباشرة من ثماني دقائق: أربع لعرض البطاقة والقياس والإفصاح، وأربع يعيد فيها المشارك تشغيل الدفتر ويشرح خطوة تحليل وقرار فرز يختارهما المراجع. القوالب: `labs/files/redesign_card_template.txt` و`labs/files/disclosure_template.txt`.

يُقيَّم المشروع في جلسة المراجعة (`slides/review.html`) بخمسة معايير: القياس على خط الأساس وتنفيذين 22، وإعادة التصميم 16، وتتبّع المراجع والأرقام 20، والإفصاح وفق سياسة المجلة المسمّاة 20، والمراجعة المباشرة 22. المعايير الأربعة الأولى تقابل وزن البطاقة والإفصاح (35%) في نتيجة المقرر، والخامس وزن المراجعة المباشرة (10%). تبدأ الجلسة بالفحص الفردي، ثم المراجعات.

<!-- academy:labs -->
## المختبرات

كل مختبر صفحة في `labs/` تُفتح من صفحة المقرر ومن شريحة المختبر في جلسته.

| | الجلسة | المختبر | الملف |
|---|---|---|---|
| 1.1 | اليوم 1 · الجلسة 1 | تصنيف اثني عشر استخدامًا | [`D1_1_classify_uses.html`](labs/D1_1_classify_uses.html) |
| 1.2 | اليوم 1 · الجلسة 2 | استدعاء المساعد على خمسين سجلًا | [`D1_2_screening_recall.html`](labs/D1_2_screening_recall.html) |
| 2.1 | اليوم 2 · الجلسة 1 | تدقيق عشرة ملخصات | [`D2_1_audit_summaries.html`](labs/D2_1_audit_summaries.html) |
| 2.2 | اليوم 2 · الجلسة 2 | تحليل يُعاد تشغيله نظيفًا | [`D2_2_clean_rerun.html`](labs/D2_2_clean_rerun.html) |
<!-- /academy:labs -->

## المتطلبات السابقة

- USE-FLU-201 العمل مع المساعدات الذكية: التفويض والوصف والحكم وتحمل المسؤولية
- شارك في مشروع بحثي ويستطيع تشغيل دفتر (notebook) معدّ مسبقًا

<!-- academy:tools -->
## الأدوات

كل سطر قدرة، والأمثلة قابلة للتبديل.

- **البحث العلمي والبيانات الوصفية:** OpenAlex, Crossref, PubMed
- **الفرز وإدارة المراجع:** ASReview, Zotero, JabRef
- **دفتر التحليل:** Jupyter, R مع Quarto
<!-- /academy:tools -->

<!-- academy:sources -->
## المصادر

### المرجعيات الوطنية

- [نظام حماية البيانات الشخصية](https://sdaia.gov.sa/ar/SDAIA/about/Documents/PersonalDataProtectionLawAr.pdf)
- [اللائحة التنفيذية لنظام حماية البيانات الشخصية](https://sdaia.gov.sa/ar/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLawAr.pdf)
- [القواعد العامة للاستخدام الثانوي للبيانات (النسخة الإنجليزية)](https://sdaia.gov.sa/Documents/GeneralRulesForSecondaryUseOfData_EN.pdf)
- [سياسة تصنيف البيانات](https://sdaia.gov.sa/ar/SDAIA/about/Documents/DataClassificationPolicyAr.pdf)
- [مبادئ أخلاقيات الذكاء الاصطناعي (سدايا)](https://sdaia.gov.sa/ar/SDAIA/about/Documents/ai-principles.pdf)
- [صفحة الأنظمة والسياسات في موقع سدايا](https://sdaia.gov.sa/ar/SDAIA/about/Pages/RegulationsAndPolicies.aspx)

### سياسات النشر والإفصاح

- [ICMJE Recommendations: Artificial Intelligence (AI)](https://www.icmje.org/recommendations/browse/artificial-intelligence/)
- [ICMJE Recommendations: AI Use by Authors](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html)
- [ICMJE Recommendations: AI Use by Reviewers](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-reviewers.html)
- [PLOS ONE: Ethical Publishing Practice (Artificial Intelligence Tools and Technologies)](https://journals.plos.org/plosone/s/ethical-publishing-practice)
- [Elsevier: Generative AI policies for journals](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals)

### البحث في الأدبيات والفرز

- [Rethlefsen et al.: PRISMA-S, an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7839230/)
- [PRISMA for Scoping Reviews (PRISMA-ScR)](https://www.prisma-statement.org/scoping)
- [Boetje and van de Schoot: The SAFE procedure, a practical stopping heuristic for active learning-based screening (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10908130/)
- [Walters and Wilder: Fabrication and errors in the bibliographic citations generated by ChatGPT (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/)
- [Crossref: Retraction Watch data](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/)

### الملخصات والتحليل

- [Peters and Chin-Yee: Generalization bias in large language model summarization of scientific research (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12042776/)
- [Gelman and Loken: The garden of forking paths (2013)](https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf)

### البيانات العامة

- [NASA POWER: Referencing](https://power.larc.nasa.gov/docs/referencing/)
- [NASA POWER: API documentation](https://power.larc.nasa.gov/docs/services/api/)
- [NASA Earthdata: Data Use Guidance](https://www.earthdata.nasa.gov/engage/open-data-services-software-policies/data-use-guidance)

### الأدوات

- [OpenAlex: API overview](https://help.openalex.org/how-to-use-the-api/api-overview)
- [Crossref: REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [PubMed User Guide](https://pubmed.ncbi.nlm.nih.gov/help/)
- [ASReview LAB: AI models](https://asreview.readthedocs.io/en/stable/lab/models.html)
- [Zotero](https://www.zotero.org/)
- [JabRef](https://www.jabref.org/)
- [Project Jupyter](https://jupyter.org/)
- [Quarto](https://quarto.org/)
<!-- /academy:sources -->

### المرجعيات الوطنية

يستشهد المقرر بهذه المراجع باسمها وعنوانها الرسمي، ولا ينقل من نصوصها. من عنده بيانات حقيقية يرجع إلى النص الرسمي وإلى الجهة المختصة في منشأته.

- نظام حماية البيانات الشخصية: https://sdaia.gov.sa/ar/SDAIA/about/Documents/PersonalDataProtectionLawAr.pdf
- اللائحة التنفيذية لنظام حماية البيانات الشخصية: https://sdaia.gov.sa/ar/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLawAr.pdf
- القواعد العامة للاستخدام الثانوي للبيانات (النسخة الإنجليزية): https://sdaia.gov.sa/Documents/GeneralRulesForSecondaryUseOfData_EN.pdf
- سياسة تصنيف البيانات: https://sdaia.gov.sa/ar/SDAIA/about/Documents/DataClassificationPolicyAr.pdf
- مبادئ أخلاقيات الذكاء الاصطناعي الصادرة عن سدايا: https://sdaia.gov.sa/ar/SDAIA/about/Documents/ai-principles.pdf
- نظام أخلاقيات البحث على المخلوقات الحية ولائحته التنفيذية: لم يُعثر على عنوان رسمي لنصه يوم إعداد المقرر، فيُذكر هنا باسمه. يُطلب نصه النافذ من لجنة أخلاقيات البحث في المنشأة.
- النسخة العربية من القواعد العامة للاستخدام الثانوي للبيانات ومن بقية الوثائق: صفحة الأنظمة والسياسات في موقع سدايا، https://sdaia.gov.sa/ar/SDAIA/about/Pages/RegulationsAndPolicies.aspx
