export type LocaleDirection = 'ltr' | 'rtl';

export type LocaleDefinition = {
  code: string;
  label: string;
  nativeLabel: string;
  dir: LocaleDirection;
};

export const locales: LocaleDefinition[] = [
  { code: 'en', label: 'English', nativeLabel: 'English', dir: 'ltr' },
  { code: 'ur', label: 'Urdu', nativeLabel: 'اردو', dir: 'rtl' },
  { code: 'ar', label: 'Arabic', nativeLabel: 'العربية', dir: 'rtl' },
  { code: 'ru', label: 'Russian', nativeLabel: 'Русский', dir: 'ltr' },
  { code: 'fr', label: 'French', nativeLabel: 'Français', dir: 'ltr' },
  { code: 'pt', label: 'Portuguese', nativeLabel: 'Português', dir: 'ltr' },
  { code: 'de', label: 'German', nativeLabel: 'Deutsch', dir: 'ltr' },
  { code: 'es', label: 'Spanish', nativeLabel: 'Español', dir: 'ltr' },
  { code: 'tr', label: 'Turkish', nativeLabel: 'Türkçe', dir: 'ltr' },
  { code: 'zh', label: 'Chinese', nativeLabel: '中文', dir: 'ltr' },
  { code: 'hi', label: 'Hindi', nativeLabel: 'हिन्दी', dir: 'ltr' },
  { code: 'bn', label: 'Bengali', nativeLabel: 'বাংলা', dir: 'ltr' },
  { code: 'id', label: 'Indonesian', nativeLabel: 'Bahasa Indonesia', dir: 'ltr' },
  { code: 'ja', label: 'Japanese', nativeLabel: '日本語', dir: 'ltr' },
];

export const defaultLocale = 'en';

export type TranslationBundle = {
  brand: string;
  tagline: string;
  heroBadge: string;
  heroTitle: string;
  heroDescription: string;
  featureGroundedTitle: string;
  featureGroundedText: string;
  featureIngestionTitle: string;
  featureIngestionText: string;
  featureScholarTitle: string;
  featureScholarText: string;
  signIn: string;
  createAccount: string;
  emailLabel: string;
  passwordLabel: string;
  loadingLogin: string;
  loginError: string;
  or: string;
  noAccount: string;
  registerTitle: string;
  registerPlaceholder: string;
  footer: string;
  languageLabel: string;
};

const translations: Record<string, TranslationBundle> = {
  en: {
    brand: 'Library Platform',
    tagline: 'Scholarly AI learning for Arabic and Islamic books',
    heroBadge: 'Multi-language scholarly AI platform',
    heroTitle: 'A learning library grounded in sources, not guesswork',
    heroDescription:
      'A production-minded platform for Arabic and Islamic books with guided ingestion, source-grounded answers, scholar review workflows, and institute-aware learning journeys.',
    featureGroundedTitle: 'Grounded Answers',
    featureGroundedText:
      'Answers are designed to cite books, preserve provenance, and carry visible verification status.',
    featureIngestionTitle: 'Guided Ingestion',
    featureIngestionText:
      'Uploads move through metadata review, AI pre-analysis, extraction, and publishing stages instead of blind chunking.',
    featureScholarTitle: 'Scholar Workflow',
    featureScholarText:
      'Sensitive domains can be reviewed, corrected, supported, or disputed with explicit trust signals.',
    signIn: 'Sign In',
    createAccount: 'Create Account',
    emailLabel: 'Email Address',
    passwordLabel: 'Password',
    loadingLogin: 'Signing in...',
    loginError: 'Login failed. Please check your credentials.',
    or: 'Or',
    noAccount: "Don't have an account?",
    registerTitle: 'Create a new account',
    registerPlaceholder: 'Registration form coming soon',
    footer: '© 2026 Library Platform. All rights reserved.',
    languageLabel: 'Language',
  },
  ur: {
    brand: 'لائبریری پلیٹ فارم',
    tagline: 'عربی اور اسلامی کتب کے لیے علمی AI نظام',
    heroBadge: 'کثیر لسانی علمی AI پلیٹ فارم',
    heroTitle: 'ایک تعلیمی لائبریری جو اندازے نہیں بلکہ مآخذ پر قائم ہے',
    heroDescription:
      'عربی اور اسلامی کتب کے لیے ایسا پلیٹ فارم جو رہنمائی شدہ انٹیک، ماخذ پر مبنی جوابات، علما کے جائزہ نظام، اور ادارہ جاتی تعلیمی سفر فراہم کرتا ہے۔',
    featureGroundedTitle: 'ماخذ پر مبنی جوابات',
    featureGroundedText:
      'جوابات کتابی حوالے، ماخذی ثبوت، اور نمایاں توثیقی حالت کے ساتھ تیار کیے جاتے ہیں۔',
    featureIngestionTitle: 'رہنمائی شدہ انٹیک',
    featureIngestionText:
      'اپ لوڈز اندھا دھند چنکنگ کے بجائے میٹاڈیٹا جائزہ، AI تجزیہ، استخراج اور اشاعت کے مراحل سے گزرتے ہیں۔',
    featureScholarTitle: 'علما ورک فلو',
    featureScholarText:
      'حساس موضوعات کو واضح اعتماد اشاروں کے ساتھ جائزہ، تصحیح، تائید یا اختلاف کے لیے پیش کیا جا سکتا ہے۔',
    signIn: 'سائن اِن',
    createAccount: 'اکاؤنٹ بنائیں',
    emailLabel: 'ای میل',
    passwordLabel: 'پاس ورڈ',
    loadingLogin: 'سائن اِن ہو رہا ہے...',
    loginError: 'لاگ اِن ناکام ہوا۔ براہ کرم اپنی معلومات دوبارہ چیک کریں۔',
    or: 'یا',
    noAccount: 'اکاؤنٹ نہیں ہے؟',
    registerTitle: 'نیا اکاؤنٹ بنائیں',
    registerPlaceholder: 'رجسٹریشن فارم جلد دستیاب ہوگا',
    footer: '© 2026 لائبریری پلیٹ فارم۔ جملہ حقوق محفوظ ہیں۔',
    languageLabel: 'زبان',
  },
  ar: {
    brand: 'مكتبة النحو',
    tagline: 'منصة تعليمية ذكية للكتب الإسلامية والعربية',
    heroBadge: 'منصة علمية متعددة اللغات',
    heroTitle: 'مكتبة تعليمية مبنية على المصادر لا على التخمين',
    heroDescription:
      'منصة إنتاجية للكتب العربية والإسلامية مع مسار رفع موجّه، وإجابات موثقة بالمصادر، وسير عمل مراجعة العلماء، وتجربة تعليمية تراعي المؤسسة.',
    featureGroundedTitle: 'إجابات موثقة',
    featureGroundedText:
      'الإجابات مصممة لتعرض الكتب والمراجع وسجل التوثيق وحالة التحقق بشكل واضح.',
    featureIngestionTitle: 'إدخال موجّه',
    featureIngestionText:
      'تمر الملفات بمراجعة بيانات وصفية وتحليل أولي واستخراج ومراجعة ونشر بدل الرفع العشوائي.',
    featureScholarTitle: 'سير عمل العلماء',
    featureScholarText:
      'يمكن مراجعة الموضوعات الحساسة وتصحيحها ودعمها أو الاعتراض عليها مع شارات ثقة واضحة.',
    signIn: 'دخول',
    createAccount: 'إنشاء حساب',
    emailLabel: 'البريد الإلكتروني',
    passwordLabel: 'كلمة المرور',
    loadingLogin: 'جاري تسجيل الدخول...',
    loginError: 'فشل تسجيل الدخول. يرجى التحقق من بياناتك.',
    or: 'أو',
    noAccount: 'ليس لديك حساب؟',
    registerTitle: 'إنشاء حساب جديد',
    registerPlaceholder: 'نموذج التسجيل قادم قريبًا',
    footer: '© 2026 مكتبة النحو. جميع الحقوق محفوظة.',
    languageLabel: 'اللغة',
  },
  ru: {
    brand: 'Библиотека знаний',
    tagline: 'Научная AI-платформа для арабских и исламских книг',
    heroBadge: 'Многоязычная научная AI-платформа',
    heroTitle: 'Учебная библиотека, основанная на источниках, а не на догадках',
    heroDescription:
      'Платформа для арабских и исламских книг с управляемой загрузкой, ответами с опорой на источники, экспертной проверкой и учебными сценариями для институтов.',
    featureGroundedTitle: 'Ответы с источниками',
    featureGroundedText:
      'Ответы сопровождаются ссылками на книги, происхождением данных и статусом проверки.',
    featureIngestionTitle: 'Управляемая загрузка',
    featureIngestionText:
      'Загрузка проходит через метаданные, AI-анализ, извлечение, проверку и публикацию.',
    featureScholarTitle: 'Проверка учёными',
    featureScholarText:
      'Чувствительные темы можно проверять, исправлять, поддерживать или оспаривать с явными маркерами доверия.',
    signIn: 'Войти',
    createAccount: 'Создать аккаунт',
    emailLabel: 'Эл. почта',
    passwordLabel: 'Пароль',
    loadingLogin: 'Вход...',
    loginError: 'Не удалось войти. Проверьте учетные данные.',
    or: 'Или',
    noAccount: 'Нет аккаунта?',
    registerTitle: 'Создать новый аккаунт',
    registerPlaceholder: 'Форма регистрации скоро появится',
    footer: '© 2026 Library Platform. Все права защищены.',
    languageLabel: 'Язык',
  },
  fr: {
    brand: 'Library Platform',
    tagline: 'Plateforme savante IA pour les livres arabes et islamiques',
    heroBadge: 'Plateforme savante multilingue',
    heroTitle: 'Une bibliothèque d’apprentissage fondée sur les sources, pas sur l’imagination',
    heroDescription:
      'Une plateforme moderne pour les livres arabes et islamiques avec ingestion guidée, réponses fondées sur les sources, validation savante et parcours d’apprentissage institutionnels.',
    featureGroundedTitle: 'Réponses fondées',
    featureGroundedText:
      'Les réponses citent les livres, conservent la provenance et affichent l’état de vérification.',
    featureIngestionTitle: 'Ingestion guidée',
    featureIngestionText:
      'Les uploads passent par métadonnées, pré-analyse IA, extraction, revue et publication.',
    featureScholarTitle: 'Workflow savant',
    featureScholarText:
      'Les sujets sensibles peuvent être relus, corrigés, soutenus ou contestés avec des signaux de confiance clairs.',
    signIn: 'Se connecter',
    createAccount: 'Créer un compte',
    emailLabel: 'Adresse e-mail',
    passwordLabel: 'Mot de passe',
    loadingLogin: 'Connexion...',
    loginError: 'Échec de connexion. Vérifiez vos identifiants.',
    or: 'Ou',
    noAccount: "Vous n'avez pas de compte ?",
    registerTitle: 'Créer un nouveau compte',
    registerPlaceholder: "Le formulaire d'inscription arrive bientôt",
    footer: '© 2026 Library Platform. Tous droits réservés.',
    languageLabel: 'Langue',
  },
  pt: {
    brand: 'Library Platform',
    tagline: 'Plataforma acadêmica de IA para livros árabes e islâmicos',
    heroBadge: 'Plataforma acadêmica multilíngue',
    heroTitle: 'Uma biblioteca de aprendizagem baseada em fontes, não em suposições',
    heroDescription:
      'Uma plataforma moderna para livros árabes e islâmicos com ingestão guiada, respostas fundamentadas em fontes, revisão acadêmica e jornadas de aprendizagem institucionais.',
    featureGroundedTitle: 'Respostas fundamentadas',
    featureGroundedText:
      'As respostas citam livros, preservam a procedência e exibem estado de verificação.',
    featureIngestionTitle: 'Ingestão guiada',
    featureIngestionText:
      'Os uploads passam por metadados, pré-análise por IA, extração, revisão e publicação.',
    featureScholarTitle: 'Fluxo de revisão acadêmica',
    featureScholarText:
      'Temas sensíveis podem ser revisados, corrigidos, apoiados ou contestados com sinais claros de confiança.',
    signIn: 'Entrar',
    createAccount: 'Criar conta',
    emailLabel: 'E-mail',
    passwordLabel: 'Senha',
    loadingLogin: 'Entrando...',
    loginError: 'Falha no login. Verifique suas credenciais.',
    or: 'Ou',
    noAccount: 'Não tem conta?',
    registerTitle: 'Criar nova conta',
    registerPlaceholder: 'Formulário de cadastro em breve',
    footer: '© 2026 Library Platform. Todos os direitos reservados.',
    languageLabel: 'Idioma',
  },
  de: {
    brand: 'Library Platform',
    tagline: 'Wissenschaftliche KI-Plattform für arabische und islamische Bücher',
    heroBadge: 'Mehrsprachige wissenschaftliche KI-Plattform',
    heroTitle: 'Eine Lernbibliothek auf Quellenbasis statt Vermutungen',
    heroDescription:
      'Eine moderne Plattform für arabische und islamische Bücher mit geführter Aufnahme, quellenbasierten Antworten, Gelehrtenprüfung und institutsbezogenen Lernpfaden.',
    featureGroundedTitle: 'Quellenbasierte Antworten',
    featureGroundedText:
      'Antworten zitieren Bücher, bewahren Herkunftsdaten und zeigen den Prüfstatus klar an.',
    featureIngestionTitle: 'Geführte Aufnahme',
    featureIngestionText:
      'Uploads durchlaufen Metadaten, KI-Voranalyse, Extraktion, Prüfung und Veröffentlichung.',
    featureScholarTitle: 'Gelehrten-Workflow',
    featureScholarText:
      'Sensible Themen können mit klaren Vertrauenssignalen geprüft, korrigiert, unterstützt oder beanstandet werden.',
    signIn: 'Anmelden',
    createAccount: 'Konto erstellen',
    emailLabel: 'E-Mail-Adresse',
    passwordLabel: 'Passwort',
    loadingLogin: 'Anmeldung läuft...',
    loginError: 'Anmeldung fehlgeschlagen. Bitte prüfen Sie Ihre Zugangsdaten.',
    or: 'Oder',
    noAccount: 'Noch kein Konto?',
    registerTitle: 'Neues Konto erstellen',
    registerPlaceholder: 'Registrierungsformular folgt in Kürze',
    footer: '© 2026 Library Platform. Alle Rechte vorbehalten.',
    languageLabel: 'Sprache',
  },
  es: {
    brand: 'Library Platform',
    tagline: 'Plataforma académica de IA para libros árabes e islámicos',
    heroBadge: 'Plataforma académica multilingüe',
    heroTitle: 'Una biblioteca de aprendizaje basada en fuentes, no en suposiciones',
    heroDescription:
      'Una plataforma moderna para libros árabes e islámicos con ingestión guiada, respuestas fundamentadas en fuentes, revisión académica y recorridos de aprendizaje institucionales.',
    featureGroundedTitle: 'Respuestas fundamentadas',
    featureGroundedText:
      'Las respuestas citan libros, preservan la procedencia y muestran el estado de verificación.',
    featureIngestionTitle: 'Ingesta guiada',
    featureIngestionText:
      'Las cargas pasan por metadatos, preanálisis con IA, extracción, revisión y publicación.',
    featureScholarTitle: 'Flujo académico',
    featureScholarText:
      'Los temas sensibles pueden revisarse, corregirse, apoyarse o disputarse con señales claras de confianza.',
    signIn: 'Iniciar sesión',
    createAccount: 'Crear cuenta',
    emailLabel: 'Correo electrónico',
    passwordLabel: 'Contraseña',
    loadingLogin: 'Iniciando sesión...',
    loginError: 'Error de inicio de sesión. Verifica tus credenciales.',
    or: 'O',
    noAccount: '¿No tienes cuenta?',
    registerTitle: 'Crear una nueva cuenta',
    registerPlaceholder: 'El formulario de registro estará disponible pronto',
    footer: '© 2026 Library Platform. Todos los derechos reservados.',
    languageLabel: 'Idioma',
  },
  tr: {
    brand: 'Library Platform',
    tagline: 'Arapça ve İslami kitaplar için akademik yapay zeka platformu',
    heroBadge: 'Çok dilli akademik yapay zeka platformu',
    heroTitle: 'Tahmine değil kaynaklara dayanan bir öğrenme kütüphanesi',
    heroDescription:
      'Arapça ve İslami kitaplar için yönlendirilmiş içe aktarma, kaynak temelli cevaplar, alim incelemesi ve kurum odaklı öğrenme akışları sunan modern bir platform.',
    featureGroundedTitle: 'Kaynak temelli cevaplar',
    featureGroundedText:
      'Cevaplar kitaplara atıf yapar, köken bilgisini korur ve doğrulama durumunu görünür kılar.',
    featureIngestionTitle: 'Yönlendirilmiş içe aktarma',
    featureIngestionText:
      'Yüklemeler kör parçalamak yerine meta veriler, yapay zeka analizi, çıkarım, inceleme ve yayınlama aşamalarından geçer.',
    featureScholarTitle: 'Alim iş akışı',
    featureScholarText:
      'Hassas konular açık güven sinyalleriyle incelenebilir, düzeltilebilir, desteklenebilir veya itiraz edilebilir.',
    signIn: 'Giriş Yap',
    createAccount: 'Hesap Oluştur',
    emailLabel: 'E-posta',
    passwordLabel: 'Şifre',
    loadingLogin: 'Giriş yapılıyor...',
    loginError: 'Giriş başarısız. Lütfen bilgilerinizi kontrol edin.',
    or: 'Veya',
    noAccount: 'Hesabınız yok mu?',
    registerTitle: 'Yeni hesap oluştur',
    registerPlaceholder: 'Kayıt formu yakında hazır olacak',
    footer: '© 2026 Library Platform. Tüm hakları saklıdır.',
    languageLabel: 'Dil',
  },
};

const englishFallback = translations.en;

export function getLocaleDefinition(locale?: string): LocaleDefinition {
  return locales.find((item) => item.code === locale) ?? locales[0];
}

export function getTranslations(locale?: string): TranslationBundle {
  return translations[locale ?? defaultLocale] ?? englishFallback;
}

export function isRtlLocale(locale?: string): boolean {
  return getLocaleDefinition(locale).dir === 'rtl';
}
