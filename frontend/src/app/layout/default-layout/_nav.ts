import { INavData } from '@coreui/angular';

export const navItems: INavData[] = [
  {
    name: 'Dashboard',
    url: '/dashboard',
    iconComponent: { name: 'cil-speedometer' },
  },
  {
    name: 'Usuários',
    url: '/users',
    iconComponent: { name: 'cil-people' },
  },
  {
    name: 'Perfil',
    url: '/profile',
    iconComponent: { name: 'cil-user' },
  },
];
