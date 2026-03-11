import React from 'react';
import { ArrowRight, CheckCircle, Shield, Plane, TrendingUp, Clock, DollarSign, Globe, HelpCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const LandingPage = () => {
  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    whileInView: { opacity: 1, y: 0 },
    viewport: { once: true },
    transition: { duration: 0.6 }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-100">
      {/* Header / Nav */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Globe className="text-blue-600 w-8 h-8" />
            <span className="font-bold text-xl tracking-tight">ParaguayFiscal</span>
          </div>
          <a href="#cta" className="hidden sm:block bg-blue-600 text-white px-6 py-2 rounded-full font-medium hover:bg-blue-700 transition-colors">
            Agendar Consultoría
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-4xl md:text-6xl font-extrabold text-slate-900 mb-6 leading-tight">
              Residencia Fiscal en Paraguay <br />
              <span className="text-blue-600 font-bold">para Extranjeros</span>
            </h1>
            <p className="text-xl md:text-2xl text-slate-600 mb-10 max-w-3xl mx-auto">
              Reduce legalmente tu carga fiscal y protege tu patrimonio en uno de los sistemas más atractivos del mundo.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="#cta" className="bg-blue-600 text-white px-8 py-4 rounded-xl text-lg font-bold hover:bg-blue-700 transition-all flex items-center justify-center gap-2 shadow-lg hover:shadow-blue-200">
                Agendar consultoría gratuita <ArrowRight className="w-5 h-5" />
              </a>
              <a href="#ventajas" className="bg-white text-slate-700 border border-slate-200 px-8 py-4 rounded-xl text-lg font-bold hover:bg-slate-50 transition-all">
                Ver ventajas fiscales
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Problema Section */}
      <section className="py-20 bg-white px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">¿Por qué salir de Europa?</h2>
            <div className="w-20 h-1 bg-red-500 mx-auto rounded-full"></div>
          </div>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="flex gap-4 p-6 bg-slate-50 rounded-2xl border border-slate-100">
                <div className="bg-red-100 p-3 rounded-full h-fit text-red-600">
                  <TrendingUp className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">Presión fiscal asfixiante</h3>
                  <p className="text-slate-600">Europa está aumentando impuestos y el control fiscal sobre empresarios y ahorradores de forma agresiva.</p>
                </div>
              </div>
              <div className="flex gap-4 p-6 bg-slate-50 rounded-2xl border border-slate-100">
                <div className="bg-red-100 p-3 rounded-full h-fit text-red-600">
                  <Shield className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">Falta de seguridad jurídica</h3>
                  <p className="text-slate-600">Cambios constantes en las reglas del juego que ponen en riesgo tu patrimonio y planificación a largo plazo.</p>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="bg-blue-600/5 absolute -inset-4 rounded-3xl -rotate-2"></div>
              <div className="relative bg-white p-8 rounded-3xl border border-slate-200 shadow-xl">
                <blockquote className="text-lg italic text-slate-700">
                  "Muchos empresarios están atrapados en sistemas que penalizan el éxito. Paraguay es la alternativa legal y estratégica para proteger el fruto de tu trabajo."
                </blockquote>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Solución Section */}
      <section className="py-20 bg-blue-900 text-white px-4 overflow-hidden relative">
        <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/2 w-96 h-96 bg-blue-500/20 blur-3xl rounded-full"></div>
        <div className="max-w-7xl mx-auto relative">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">La Solución: Paraguay</h2>
            <p className="text-blue-100 text-lg">Un refugio de libertad fiscal en el corazón de Sudamérica.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20">
              <h3 className="text-4xl font-bold mb-4 text-blue-300">10%</h3>
              <p className="font-bold mb-2">Impuesto de tipo único (Flat Tax)</p>
              <p className="text-blue-100/80">IVA, Impuesto a la Renta Personal y Empresarial limitados a un máximo del 10%.</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20">
              <h3 className="text-4xl font-bold mb-4 text-blue-300">0%</h3>
              <p className="font-bold mb-2">Sistema Territorial</p>
              <p className="text-blue-100/80">Tus ingresos generados fuera de Paraguay están legalmente exentos de impuestos locales.</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm p-8 rounded-2xl border border-white/20">
              <h3 className="text-4xl font-bold mb-4 text-blue-300">Fast</h3>
              <p className="font-bold mb-2">Proceso Ágil</p>
              <p className="text-blue-100/80">Obtención de residencia permanente y cédula de identidad en tiempo récord comparado con otros países.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Proceso Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Tu camino a la libertad fiscal</h2>
            <p className="text-slate-600">Acompañamiento integral en cada paso del proceso.</p>
          </div>
          <div className="grid md:grid-cols-4 gap-4">
            {[
              { step: "1", title: "Evaluación del caso", desc: "Analizamos tu situación actual y planificamos la salida fiscal legal.", icon: Globe },
              { step: "2", title: "Viaje a Paraguay", desc: "Te recibimos en Asunción para realizar los trámites presenciales.", icon: Plane },
              { step: "3", title: "Tramitación", desc: "Gestión completa de tu residencia permanente y cédula ante migraciones.", icon: Shield },
              { step: "4", title: "Optimización", desc: "Configuración de tu estructura fiscal para maximizar el ahorro legal.", icon: TrendingUp }
            ].map((item, idx) => (
              <motion.div
                key={idx}
                {...fadeInUp}
                className="relative p-8 bg-white border border-slate-200 rounded-3xl hover:border-blue-500 transition-all group"
              >
                <div className="text-5xl font-black text-slate-100 absolute top-4 right-6 group-hover:text-blue-50/50 transition-colors">0{item.step}</div>
                <div className="bg-blue-600 text-white p-3 rounded-2xl w-fit mb-6 relative z-10">
                  <item.icon className="w-6 h-6" />
                </div>
                <h4 className="text-xl font-bold mb-2 relative z-10">{item.title}</h4>
                <p className="text-slate-600 relative z-10">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Ventajas Section */}
      <section id="ventajas" className="py-20 bg-slate-900 text-white px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl md:text-5xl font-bold mb-8 leading-tight">Ventajas competitivas de Paraguay</h2>
              <ul className="space-y-6">
                <li className="flex gap-4">
                  <CheckCircle className="text-blue-400 w-6 h-6 shrink-0" />
                  <div>
                    <span className="font-bold text-lg block">Impuestos bajos</span>
                    <span className="text-slate-400">Máximo del 10% en rentas locales y consumo.</span>
                  </div>
                </li>
                <li className="flex gap-4">
                  <CheckCircle className="text-blue-400 w-6 h-6 shrink-0" />
                  <div>
                    <span className="font-bold text-lg block">Sistema territorial real</span>
                    <span className="text-slate-400">Tus dividendos y rentas extranjeras no tributan.</span>
                  </div>
                </li>
                <li className="flex gap-4">
                  <CheckCircle className="text-blue-400 w-6 h-6 shrink-0" />
                  <div>
                    <span className="font-bold text-lg block">Proceso rápido</span>
                    <span className="text-slate-400">Residencia permanente en pocos meses.</span>
                  </div>
                </li>
                <li className="flex gap-4">
                  <CheckCircle className="text-blue-400 w-6 h-6 shrink-0" />
                  <div>
                    <span className="font-bold text-lg block">Costo de vida</span>
                    <span className="text-slate-400">Calidad de vida premium a una fracción del costo europeo.</span>
                  </div>
                </li>
              </ul>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/5 p-8 rounded-3xl border border-white/10 text-center">
                <Clock className="w-10 h-10 mx-auto mb-4 text-blue-400" />
                <div className="text-3xl font-bold mb-1">90 días</div>
                <div className="text-sm text-slate-400">Proceso estimado</div>
              </div>
              <div className="bg-white/5 p-8 rounded-3xl border border-white/10 text-center mt-8">
                <DollarSign className="w-10 h-10 mx-auto mb-4 text-blue-400" />
                <div className="text-3xl font-bold mb-1">10%</div>
                <div className="text-sm text-slate-400">Flat Tax</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 flex items-center justify-center gap-3">
               <HelpCircle className="text-blue-600" /> Preguntas Frecuentes
            </h2>
          </div>
          <div className="space-y-6">
            {[
              { q: "¿Es legal?", a: "Absolutamente. Paraguay ofrece este marco legal para atraer inversión. Todo el proceso se realiza bajo las leyes de migración y tributarias vigentes tanto en Paraguay como siguiendo convenios internacionales." },
              { q: "¿Cuánto tarda el proceso?", a: "La obtención de la residencia permanente suele demorar entre 3 y 5 meses, aunque puedes obtener tu número de identificación provisorio mucho antes." },
              { q: "¿Cuánto cuesta?", a: "Los costos varían según el número de aplicantes y la complejidad del caso. Agenda una consultoría para recibir un presupuesto detallado a tu medida." },
              { q: "¿Debo vivir en Paraguay todo el año?", a: "Para mantener la residencia permanente solo se requiere visitar el país una vez al año, aunque para la residencia fiscal existen requisitos específicos de presencia que analizaremos en tu caso." }
            ].map((faq, idx) => (
              <div key={idx} className="p-6 border border-slate-200 rounded-2xl hover:bg-slate-50 transition-colors">
                <h4 className="text-lg font-bold mb-2">{faq.q}</h4>
                <p className="text-slate-600">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Final / Form */}
      <section id="cta" className="py-20 px-4 bg-blue-600 text-white">
        <div className="max-w-5xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-5xl font-bold mb-6">¿Listo para dar el paso?</h2>
              <p className="text-xl text-blue-100 mb-8">
                Agenda hoy mismo una sesión estratégica para evaluar tu situación fiscal y diseñar tu plan de salida.
              </p>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="bg-white/20 p-2 rounded-full"><CheckCircle className="w-5 h-5" /></div>
                  <span>Sesión personalizada 1 a 1</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="bg-white/20 p-2 rounded-full"><CheckCircle className="w-5 h-5" /></div>
                  <span>Análisis de ahorro potencial</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="bg-white/20 p-2 rounded-full"><CheckCircle className="w-5 h-5" /></div>
                  <span>Plan de acción paso a paso</span>
                </div>
              </div>
            </div>
            <div className="bg-white p-8 rounded-3xl shadow-2xl text-slate-900">
              <h3 className="text-2xl font-bold mb-6">Solicitar Consultoría</h3>
              <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Nombre Completo</label>
                  <input type="text" className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all" placeholder="Juan Pérez" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Email Corporativo</label>
                  <input type="email" className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all" placeholder="juan@empresa.com" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">País de Residencia Actual</label>
                  <select className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all">
                    <option>España</option>
                    <option>México</option>
                    <option>Argentina</option>
                    <option>Otro</option>
                  </select>
                </div>
                <button className="w-full bg-blue-600 text-white font-bold py-4 rounded-xl hover:bg-blue-700 transition-all shadow-lg shadow-blue-200">
                  Enviar solicitud ahora
                </button>
                <p className="text-xs text-center text-slate-500">Privacidad garantizada. No compartimos tus datos.</p>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t border-slate-200 bg-white">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex items-center gap-2">
            <Globe className="text-blue-600 w-6 h-6" />
            <span className="font-bold text-lg tracking-tight">ParaguayFiscal</span>
          </div>
          <div className="flex gap-8 text-sm text-slate-500">
            <a href="#" className="hover:text-blue-600">Aviso Legal</a>
            <a href="#" className="hover:text-blue-600">Privacidad</a>
            <a href="#" className="hover:text-blue-600">Contacto</a>
          </div>
          <p className="text-sm text-slate-400">© 2026 ParaguayFiscal. Todos los derechos reservados.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;